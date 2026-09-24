
# Extreme Weather–Transport–Economic Impact

This repository provides the code supporting the manuscript:

**Coupled transport and supply-chain networks amplify economic losses from extreme weather**

## 1. Overview

This study develops an integrated computational framework to quantify how extreme weather-induced traffic shocks propagate through transport and supply-chain networks and generate economy-wide losses.

The framework combines spatiotemporal traffic forecasting, counterfactual analysis, origin–destination (OD) estimation, and dynamic multi-regional input-output (MRIO) simulation. It is applied to New Zealand to examine the economic consequences of extreme weather under different hazard intensity, duration, and spatial exposure scenarios.

## 2. Methodological framework

The framework consists of four main components:

**1. Traffic prediction and counterfactual analysis**

A spatiotemporal graph neural network integrates historical traffic observations and weather variables to predict traffic flows. Counterfactual weather conditions are used to estimate traffic shocks attributable to extreme weather.

**2. OD estimation and traffic assignment**

Regional OD demand is estimated using regional economic activity as a prior and calibrated against observed traffic counts through user-equilibrium traffic assignment.

**3. Dynamic MRIO simulation**

Traffic shocks are incorporated into a dynamic MRIO model to simulate production disruptions, inventory constraints, order adjustments, and cascading economic losses across regions and sectors.

**4. Scenario and propagation analysis**

The framework examines the effects of hazard intensity, duration, and spatial exposure on national economic losses. It also investigates upstream and downstream supply-chain propagation.

## 3. Repository structure

The planned repository structure is:

```text
extreme-weather-transport-economic-impact/
│
├── README.md
├── requirements.txt
│
├── minimal_example/
│   ├── dynamic_mrio_example.py
│   └── data/
│       └── MRIOTtest.xlsx
│
├── traffic_prediction/
├── od_estimation/
├── dynamic_mrio/
└── scenario_analysis/
```

The `minimal_example` directory is the first component of the code release. The remaining directories will be added as the reproducibility package is prepared.

## 4. Minimal example

A small-scale dynamic MRIO simulation is provided to illustrate the core economic propagation mechanisms.

The example uses a system with four regions and three sectors per region. It simulates a temporary production-capacity shock over 40 time steps.

The simulation includes:

- Production-capacity constraints
- Inventory constraints and consumption
- Proportional order allocation
- Inventory replenishment
- Dynamic production adjustments

At each time step, sectoral output is determined by the minimum of available inventory, production capacity, and incoming orders. Inventory levels and intermediate input orders are then updated for the next time step.

### Requirements

- Python 3
- NumPy
- pandas
- Matplotlib
- openpyxl

### Usage

Run the example from the repository root:

```bash
python minimal_example/dynamic_mrio_example.py
```

The script reads `minimal_example/data/MRIOTtest.xlsx` and simulates the evolution of total economic output following a temporary production-capacity shock.

## 5. Data availability

The full study uses traffic observations, meteorological data, transport-network information, and regional economic data for New Zealand.

Some datasets may be subject to third-party access or redistribution restrictions. Their sources and preprocessing requirements will be documented where applicable.

The small-scale MRIO input file required for the minimal example is included in the repository.

## 6. Code availability

The repository is being developed to support the reproducibility of the manuscript.

The initial release contains a minimal dynamic MRIO simulation. Additional scripts for traffic prediction, OD estimation, full-scale dynamic MRIO simulation, and scenario analysis will be added as they are prepared for release.
