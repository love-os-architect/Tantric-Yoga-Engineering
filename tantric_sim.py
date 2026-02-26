# -*- coding: utf-8 -*-
"""
Tantric Engineering Simulator (Love-OS / HVS Protocol v2.0)
- Simulates the nonlinear dynamics of integration, gap charging, and phase transitions.
- Includes biological saturation limits (tanh) and irreversible OS updates (R_int decay).

Tested with: Python 3.10+, numpy, pandas, matplotlib
"""

from dataclasses import dataclass
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ========== 1. Parameter Definitions ==========

@dataclass
class TantricParams:
    # Scalar E coefficients
    alpha: float = 0.6      # Natural decay
    beta: float  = 1.0      # Sensitivity to Stimulus S(t)
    gamma: float = 0.8      # Sensitivity to Prediction Error
    delta: float = 0.7      # Impact of Internal Resistance R_int
    eta: float   = 0.15     # Noise intensity
    kappa: float = 0.3      # Contribution of V_gap during Sync

    # Biological/Hardware Limits
    E_max: float = 10.0     # Maximum emotional/energy capacity (Saturation limit)
    
    # Gap Charging (External Resistance Analogy)
    V_source: float = 5.0   # Target maximum charge
    rho: float      = 0.02  # Charge rate
    chi: float      = 0.8   # Discharge rate during Sync event

    # Irreversible Phase Transition (OS Update)
    R_int_base_init: float = 0.9  # Initial Internal Resistance
    R_int_min: float       = 0.1  # Absolute minimum physical resistance
    phase_transition_decay: float = 0.6  # Multiplier for R_int permanent drop upon successful Sync
    sync_threshold: float  = 3.0  # Minimum V_gap required to trigger an OS Update

# ========== 2. Schedules and Triggers ==========

def stimulus_schedule(t: float) -> float:
    base = 1.0 if 10 <= t < 40 else (-0.5 if 40 <= t < 60 else 0.5 if 60 <= t < 90 else 0.0)
    ripple = 0.2 * np.sin(2 * np.pi * 0.03 * t)
    return base + ripple

def prediction_error(t: float) -> float:
    bumps = [(25, 5.0, 1.2), (55, 6.0, 1.8), (80, 4.0, 1.5)]
    val = sum(h * np.exp(-0.5 * ((t - c) / w)**2) for c, w, h in bumps)
    return val

def sync_event(t: float) -> float:
    triggers = [45, 90] # Sync windows
    width = 3.0
    return 1.0 if any(abs(t - c) <= width/2 for c in triggers) else 0.0

def calculate_transient_R_int(t: float, current_base: float) -> float:
    # Transient ego rebounds over time, but bounded by the current structural base
    rebound = 0.2 * np.exp(-0.5 * ((t - 65) / 4)**2) 
    return current_base + rebound

# ========== 3. Core Simulator ==========

def simulate(params: TantricParams, T: float = 120.0, dt: float = 0.1, seed: int = 42):
    rng = np.random.default_rng(seed)
    steps = int(T / dt) + 1

    E = 0.0
    V_gap = 0.0
    current_R_int_base = params.R_int_base_init
    
    records = []

    for i in range(steps):
        t = i * dt

        S = stimulus_schedule(t)
        pe = prediction_error(t)
        sync = sync_event(t)
        noise = rng.normal(0.0, 1.0)

        # 1. Calculate current internal resistance
        R_int = calculate_transient_R_int(t, current_base=current_R_int_base)

        # 2. Phase Transition (Irreversible OS Update)
        # If a Sync happens AND we have enough charged voltage, the system structurally upgrades
        if sync > 0.5 and V_gap > params.sync_threshold:
            current_R_int_base = max(params.R_int_min, current_R_int_base * params.phase_transition_decay)

        # 3. Gap Voltage Update (Charging & Discharging)
        dVgap = params.rho * (params.V_source - V_gap) - params.chi * sync
        V_gap = max(0.0, V_gap + dVgap * dt)

        # 4. Energy Dynamics with Saturation (tanh)
        dE = (
            -params.alpha * E
            + params.beta * S
            + params.gamma * pe
            - params.delta * Rint
            + params.eta * noise
            + params.kappa * (V_gap if sync > 0.5 else 0) # V_gap energy flows into E only during Sync
        )
        
        # Apply biological/hardware saturation limit
        E_unbounded = E + dE * dt
        E = params.E_max * np.tanh(E_unbounded / params.E_max)

        records.append({
            "t": t,
            "E": E,
            "V_gap": V_gap,
            "R_int_structural": current_R_int_base,
            "R_int_actual": R_int,
            "Sync": sync
        })

    return pd.DataFrame(records)

# ========== 4. Visualization & Export ==========

def plot_results(df: pd.DataFrame):
    plt.figure(figsize=(10, 8))

    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(df["t"], df["E"], label="E (Integrated Energy)", color="#1f77b4", linewidth=2)
    ax1.set_ylabel("Energy E")
    ax1.legend(loc="upper right")
    ax1.grid(True, alpha=0.3)
    ax1.set_title("Tantric Engineering: HVS Protocol Dynamics", fontsize=12)

    ax2 = plt.subplot(3, 1, 2, sharex=ax1)
    ax2.plot(df["t"], df["V_gap"], label="Gap Voltage (V_gap)", color="#17becf", linewidth=2)
    ax2.fill_between(df["t"], 0, df["Sync"] * df["V_gap"].max(), color="#ff7f0e", alpha=0.2, label="Sync Window")
    ax2.set_ylabel("Voltage / Sync")
    ax2.legend(loc="upper right")
    ax2.grid(True, alpha=0.3)

    ax3 = plt.subplot(3, 1, 3, sharex=ax1)
    ax3.plot(df["t"], df["R_int_actual"], label="Actual R_int (w/ transients)", color="#7f7f7f", alpha=0.7)
    ax3.plot(df["t"], df["R_int_structural"], label="Structural R_int Base (Phase Transition)", color="#d62728", linewidth=2, linestyle="--")
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Internal Resistance")
    ax3.legend(loc="upper right")
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    params = TantricParams()
    df = simulate(params, T=120.0, dt=0.1, seed=42)
    plot_results(df)
    # df.to_csv("tantric_sim_v2.csv", index=False)
