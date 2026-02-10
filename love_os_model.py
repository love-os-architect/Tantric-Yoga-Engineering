"""
Love-OS: Integration Dynamics Model
-----------------------------------
This script simulates the divergence between B-side (Ripening) 
and A-side (Quick Forcing) integration strategies.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Mathematical Components ---

def hill_function(x, x50=1.0, n=2):
    """Models the saturation of Quietness (Q)."""
    return (x**n) / (x**n + x50**n + 1e-9)

def suppression_function(r, r50=1.0, m=2):
    """Models the reduction of friction as Resistance (R) drops."""
    return (r50**m) / (r**m + r50**m + 1e-9)

def softplus_trigger(z):
    """The non-linear phase transition (Awakening) trigger."""
    return np.where(z > 20, z, np.log1p(np.exp(z)))

def calc_integration_force(Q, R, dphi, theta=0.6):
    """
    Core Love-OS Equation:
    Conditioners (Quality/Resistance/Phase) * Transition Trigger
    """
    # Weights for the internal potential
    wQ, wR, wPhi = 1.0, 1.0, 0.8
    
    conditioner = (hill_function(Q) * suppression_function(R) * ((1 + np.cos(dphi)) / 2.0)**1.0)
    
    potential = (wQ * Q - wR * R - wPhi * np.abs(dphi) - theta)
    trigger = softplus_trigger(potential)
    
    return conditioner * trigger

# --- Simulation Logic ---

def run_simulation(strategy="B-side"):
    T, dt = 80.0, 0.1
    steps = int(T / dt)
    
    t_axis = np.linspace(0, T, steps)
    F_out, PHI_out, R_out = [], [], []

    if strategy == "B-side":
        # Ripening: Moving toward high Q, low R, and 0 phase gap
        Q, R, phi = 0.5, 0.9, 1.2
        target_Q, target_R = 3.0, 0.12
        tau_Q, tau_R = 18.0, 22.0
        k0, noise_lvl = 1.2, 0.0
    else:
        # A-side: Forced Q bump, R stays high, phase is unstable
        Q, R, phi = 0.8, 0.9, 0.0
        target_Q, target_R = 1.2, 0.75
        tau_Q, tau_R = 6.0, 40.0
        k0, noise_lvl = 0.3, 0.04

    for _ in t_axis:
        # State Evolution
        Q += (target_Q - Q) * dt / tau_Q
        R += (target_R - R) * dt / tau_R
        
        # Phase dynamics (Kuramoto-like)
        coupling = k0 * hill_function(Q) * suppression_function(R)
        phi += (-coupling * np.sin(phi)) * dt + np.random.normal(0, noise_lvl)
        phi = (phi + np.pi) % (2 * np.pi) - np.pi
        
        F_out.append(calc_integration_force(Q, R, phi))
        PHI_out.append(phi)
        R_out.append(R)
        
    return t_axis, F_out, PHI_out, R_out

# --- Visualization ---

def plot_results():
    t, F_B, PHI_B, R_B = run_simulation("B-side")
    _, F_A, PHI_A, R_A = run_simulation("A-side")

    # Figure 1: Integration Force
    plt.figure(figsize=(10, 5))
    plt.plot(t, F_B, color="#5cb85c", lw=3, label="B-side: Ripening (Presence)")
    plt.plot(t, F_A, color="#d9534f", lw=2, label="A-side: Quick Forcing (Ego)")
    plt.title("Love-OS: Integration Force Evolution")
    plt.xlabel("Time (Ripening duration)")
    plt.ylabel("Force (F)")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()

    # Figure 2: Internal States
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax1.plot(t, PHI_B, color="#5cb85c", label="B-side Phase Gap")
    ax1.plot(t, PHI_A, color="#d9534f", ls='--', label="A-side Phase Gap")
    ax1.set_ylabel("Phase Gap (Δφ)")
    ax1.legend()
    
    ax2.plot(t, R_B, color="#5cb85c", label="B-side Resistance")
    ax2.plot(t, R_A, color="#d9534f", ls='--', label="A-side Resistance")
    ax2.set_ylabel("Resistance (R)")
    ax2.set_xlabel("Time")
    ax2.legend()
    plt.show()

if __name__ == "__main__":
    plot_results()
