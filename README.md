# Extreme Weather–Transport–Economic Impact

This repository provides code supporting the manuscript:

**"Coupled transport and supply-chain networks amplify economic losses from extreme weather"**

## Current release

The current version provides a minimal reproducible example of the dynamic
multi-regional input-output (MRIO) simulation used in the study.

The example demonstrates the core recursive mechanisms of the model, including:

- production-capacity shocks;
- inventory constraints;
- order allocation;
- inventory depletion and replenishment; and
- dynamic propagation of production losses.

The example uses a small 4-region × 3-sector MRIO system to illustrate the
model dynamics.

## Repository structure

```text
minimal_example/
├── dynamic_mrio_example.py
└── data/
    └── MRIOTtest.xlsx
