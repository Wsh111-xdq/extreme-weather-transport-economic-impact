import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# 参数（对应 R）

RR = 4
NN = 3
RRNN = RR * NN
UU = 1
TT = 40

# 读取 MRIOT（对应 read_excel）

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MRIOT_PATH = BASE_DIR / "data" / "MRIOTtest.xlsx"

MRIOT = pd.read_excel(
    MRIOT_PATH,
    sheet_name=0,          # R: sheet = 1
    usecols="C:R",
    skiprows=2,
    nrows=RRNN + UU,
    header=None
).to_numpy()

zz_s = MRIOT[0:RRNN, 0:RRNN] # 中间投入矩阵Z（12*12）
ff_s = MRIOT[0:RRNN, RRNN:RRNN + RR] # 最终需求矩阵F（12*4）
va_s = MRIOT[RRNN:RRNN + UU, 0:RRNN] # 增加值（1*12）
xx_s = zz_s.sum(axis=0, keepdims=True) + va_s.sum(axis=0, keepdims=True) # 总产出=Z+V（1*12）


# mat.index / mat.key

# 映射矩阵，把多个原始部门合并到库存部门
mat_index = (
    pd.read_excel(
        MRIOT_PATH,
        sheet_name=1,       # R: sheet = 2
        usecols="C:N",
        skiprows=2,
        nrows=RRNN,
        header=None
    )
    .to_numpy()
    .astype(int)
    - 1
)
print(mat_index)
no_input = mat_index.max(axis=0)

# 约束矩阵，用于限制哪些投入是可用的
mat_key = (
    pd.read_excel(
        MRIOT_PATH,
        sheet_name=4,       # R: sheet = 5
        usecols="C:N",
        skiprows=2,
        nrows=RRNN,
        header=None
    )
    .to_numpy()
    .astype(bool)
)
print(mat_key)

# merge.mat / dis.mat

# 合并投入，按 mat.index 把多个部门的投入加总到库存部门
def merge_mat(mat, mat_index):
    R, N = mat.shape
    out = np.zeros((R, N))
    for i in range(R):
        for j in range(N):
            out[mat_index[i, j], j] += mat[i, j]
    return out

# 订单分配，按技术系数 mat.ezz，将库存缺口分配回原始部门
def dis_mat(mat, mat_index, mat_ezz):
    R, N = mat.shape
    out = np.zeros((R, N))
    for i in range(R):
        for j in range(N):
            out[i, j] = mat[mat_index[i, j], j] * mat_ezz[i, j]
    return out


# 初始矩阵

zz_s_c = merge_mat(zz_s, mat_index)# 多个原始部门合并成一个库存部门
print(zz_s_c)

mat_stock = 4.0 * zz_s_c # 初始库存=4*中间使用
mat_stock_obj = mat_stock + zz_s_c # 目标库存=当前库存+中间使用

mat_order = np.hstack([zz_s, ff_s]) # 订单矩阵：中间需求矩阵+最终需求矩阵

mat_ezc = zz_s_c / xx_s #中间投入系数

mat_ezz = np.zeros((RRNN, RRNN))
for i in range(RRNN):
    for j in range(RRNN):
        mat_ezz[i, j] = zz_s[i, j] / zz_s_c[mat_index[i, j], j] # 库存的分配比例


# 冲击路径（VA_TT / FF_TT）
# 生产力下降，供给减少
VA_TT = np.ones((NN, RR, TT))

temp = np.concatenate([
    np.array([100, 100]), # 前期稳定状态，1期到2期
    np.linspace(100, 40, 4), #下降阶段，3期到6期
    np.repeat(40, 15),# 低谷，7期到21期
    np.linspace(40, 100, 4)# 恢复段，22期到25期
]) / 100

VA_TT[1, 1, :len(temp)] *= temp # 第二个区域的第二个部门受影响
print(VA_TT)
FF_TT = np.repeat(ff_s[:, :, np.newaxis], TT, axis=2)
print(FF_TT)

xx_TT = np.zeros((TT, RRNN))

for t in range(TT):
    print(t + 1)

    va_t = VA_TT[:, :, t].reshape(1, -1) # 从3D张量中提取第t期冲击

    mat_order_sum = mat_order.sum(axis=1) # 各部门接收的总订单量

    xx_t = np.zeros((1, RRNN)) # 初始化本期产出向量

    for i in range(RRNN):# 遍历每个部门i
        # 计算库存约束
        temp_raw = mat_stock[:no_input[i], i] / mat_ezc[:no_input[i], i]
        temp_raw = temp_raw[mat_key[:no_input[i], i]]

        if temp_raw.size > 0:
            temp_constraint = temp_raw.min()
        else:
            temp_constraint = np.inf

        xx_t[0, i] = min(
            temp_constraint,# 库存约束
            va_t[0, i] * xx_s[0, i], # 供给能力约束
            mat_order_sum[i] # 订单需求
        ) # 部门产出由三个约束的最小值决定

    with np.errstate(divide="ignore", invalid="ignore"):
        # 计算订单分配比例矩阵
        order_share = mat_order / mat_order_sum[:, None]
    order_share = np.nan_to_num(order_share)

    xx_t_expand = np.tile(xx_t.T, (1, RRNN + RR))
    xx_t_dis = order_share * xx_t_expand # 按比例分配产出

    mat_stock_use = np.tile(xx_t, (RRNN, 1)) * mat_ezc # 库存消耗
    mat_stock_add = merge_mat(xx_t_dis[:, :RRNN], mat_index) # 库存补充，将原始部门间的交付合并到库存部门

    mat_stock = mat_stock - mat_stock_use + mat_stock_add # 库存更新

    mat_stock_gap = mat_stock_obj - mat_stock # 订单缺口
    mat_stock_gap[mat_stock_gap < 0] = 0

    mat_order[:, :RRNN] = dis_mat(mat_stock_gap, mat_index, mat_ezz) # 将库存缺口按历史比例分配给原始供应商
    mat_order[:, RRNN:RRNN + RR] = FF_TT[:, :, t]

    xx_TT[t, :] = xx_t

plt.plot(xx_TT.sum(axis=1))
plt.xlabel("Time")
plt.ylabel("Total Output")
plt.title("Total Output Over Time")
plt.show()
