# -*- coding: utf-8 -*-
"""
Tantric Engineering Simulator v2.1 (HVS Protocol v1.1 Compliant)
- Features: H/N/S/C Metrics, Snubbed Pulse Sync, Phase Transitions.
- Presets: Buddhist (High Attention), Daoist (Low Input), Kabbalist (High Capacity).
- AB Testing: Compares "Sync-enabled" vs "No-Sync" scenarios.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class HVSParams:
    # System Coefficients
    alpha: float = 0.6      # Natural decay
    beta: float  = 1.0      # Stimulus sensitivity
    gamma: float = 0.8      # Pred-Error sensitivity
    delta: float = 0.7      # Internal Resistance impact
    kappa: float = 0.4      # Sync discharge efficiency
    
    # Presets & Baselines
    R_int_base: float = 0.9
    N_floor: float = 1.0    # Initial Noise floor
    V_source: float = 5.0   # Target charge
    C_capacity: float = 1.2 # Buffer capacity
    
    # SNUB Logic (K-pulses)
    K_pulses: int = 3
    pulse_width: float = 2.0

# --- プリセット定義 ---
PRESETS = {
    "Standard": HVSParams(),
    "Buddhist": HVSParams(alpha=0.4, delta=0.9, N_floor=0.2, gamma=1.2), # 高い注意・低ノイズ
    "Daoist":   HVSParams(beta=0.4, alpha=0.3, kappa=0.6),             # 入力最小化・自然流
    "Kabbalist":HVSParams(C_capacity=2.5, V_source=8.0, kappa=0.5)     # 高容量・高電圧
}

def simulate_hvs(params: HVSParams, enable_sync: bool = True, T: float = 100.0, dt: float = 0.1):
    steps = int(T / dt) + 1
    t_axis = np.linspace(0, T, steps)
    
    # State tracking
    E, V_gap = 0.0, 0.0
    R_int_base = params.R_int_base
    
    # Metrics
    records = []
    
    # Define Sync Windows (K pulses)
    sync_times = [30, 60, 90] if enable_sync else []
    
    for i, t in enumerate(t_axis):
        # 1. Inputs (S and Pred-Error)
        S = 1.0 if 10 <= t < 40 else 0.0
        pe = 1.5 * np.exp(-0.5 * ((t - 50)/5)**2)
        
        # 2. Sync Detection (Snubbed)
        is_sync = any(abs(t - st) <= params.pulse_width/2 for st in sync_times)
        
        # 3. R_int Dynamics (Phase Transition on successful Sync)
        if is_sync and V_gap > 3.0:
            R_int_base *= 0.85 # 不可逆的なOSアップデート
            
        R_int = R_int_base + 0.2 * np.exp(-0.5 * ((t-70)/5)**2) # Transient ego
        
        # 4. Gap Charging
        dVgap = 0.02 * (params.V_source - V_gap) - (0.8 if is_sync else 0.0)
        V_gap = max(0.0, V_gap + dVgap * dt)
        
        # 5. Energy E (tanh saturation)
        dE = -params.alpha * E + params.beta * S + params.gamma * pe - params.delta * R_int + (params.kappa * V_gap if is_sync else 0)
        E = 10.0 * np.tanh((E + dE * dt) / 10.0)
        
        records.append({"t": t, "E": E, "V_gap": V_gap, "R_int": R_int_base, "Sync": float(is_sync)})
        
    return pd.DataFrame(records)

# --- ABテストの実行と可視化 ---
def run_ab_test(preset_name="Buddhist"):
    p = PRESETS[preset_name]
    df_sync = simulate_hvs(p, enable_sync=True)
    df_no_sync = simulate_hvs(p, enable_sync=False)
    
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(df_sync["t"], df_sync["E"], label="With HVS Sync", color="blue")
    plt.plot(df_no_sync["t"], df_no_sync["E"], label="No Sync (Passive)", color="gray", linestyle="--")
    plt.title(f"AB Test: {preset_name} Mode (Energy Dynamics)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 1, 2)
    plt.plot(df_sync["t"], df_sync["R_int"], label="Structural R_int", color="red")
    plt.ylabel("System Resistance")
    plt.title("Phase Transition (OS Upgrade) Tracking")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_ab_test("Buddhist")
