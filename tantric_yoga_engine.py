This is the Python code ready for the repository. It includes the logic for the simulation we discussed.

```python
# tantric_yoga_engine.py
# Tantric Yoga Engineering (TYE) - Bio-Energy Simulation
#
# A coupled RLC circuit simulation modeling human connection dynamics.
# Implements the "Ohm's Law of Love" and "Mutual Induction" theories.

from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
@dataclass
class TYEConfig:
    T: float = 120.0           # Total simulation time [s]
    dt: float = 0.02           # Time step [s]
    
    # Circuit Parameters (L=Inductance/Potential, C=Capacity, R=Resistance/Blockage)
    L1: float = 1.0; L2: float = 1.0
    C1: float = 1.0; C2: float = 1.0
    
    # Resistance Profile (Asana Effect: Resistance decays over time)
    R_start: float = 1.0       # Stiff body / High Ego
    R_end: float = 0.12        # Relaxed body / Flow state
    tau_R: float = 30.0        # Decay time constant
    
    # Coupling Parameters
    coupling_k: float = 0.85   # Max coupling coefficient
    
    # Breath / Voltage Parameters
    V_base: float = 0.2        # Basal metabolic drive
    breath_amp: float = 0.8    # Pranayama intensity
    breath_period: float = 8.0 # Respiratory cycle [s]

cfg = TYEConfig()

# --- PHYSICS KERNEL ---

def get_alignment_factor(phase_diff_rad: float) -> float:
    """
    A(Δθ) = cos(Δθ)
    Returns +1 for alignment (Attraction), -1 for opposition (Repulsion/Runner).
    """
    return float(np.cos(np.clip(phase_diff_rad, 0, np.pi)))

def get_selection_gate(compatibility: float) -> float:
    """
    S(c): Logistic gate. 
    If compatibility is low, the circuit physically disconnects (M -> 0).
    """
    # Sigmoid function centered at 0.6
    return 1.0 / (1.0 + np.exp(-12.0 * (compatibility - 0.6)))

def run_simulation():
    # Define Scenarios
    scenarios = [
        {
            "name": "A. Twin Dynamic (Runner -> Union)", 
            "compat": 0.95, 
            "phase_schedule": "converge" # Start opposed, end aligned
        },
        {
            "name": "B. Low Compatibility (No Spark)", 
            "compat": 0.3, 
            "phase_schedule": "neutral"  # Stays orthogonal
        }
    ]
    
    # Time vector
    N = int(cfg.T / cfg.dt) + 1
    t = np.linspace(0, cfg.T, N)
    
    results = {}

    for sc in scenarios:
        # State Variables: Charge (q) and Current (I) for two bodies
        q1, I1, q2, I2 = 0.0, 0.0, 0.0, 0.0
        
        # Data Logs
        log_I1, log_I2 = np.zeros(N), np.zeros(N)
        log_M, log_Align = np.zeros(N), np.zeros(N)
        log_R = np.zeros(N)

        for i in range(N):
            ti = t[i]
            
            # 1. Hardware State: Resistance drops due to Yoga/Practice
            R_curr = cfg.R_end + (cfg.R_start - cfg.R_end) * np.exp(-ti / cfg.tau_R)
            
            # 2. Input: Voltage driven by Breath (Prana)
            V1 = cfg.V_base + cfg.breath_amp * np.sin(2 * np.pi * ti / cfg.breath_period)
            # Person 2 breathes with a slight phase shift
            V2 = cfg.V_base + cfg.breath_amp * np.sin(2 * np.pi * ti / cfg.breath_period + np.pi/6)
            
            # 3. Control Logic: Phase Alignment (The "Runner" Logic)
            if sc["phase_schedule"] == "converge":
                # Start at 140deg (Repulsion) -> Smoothly transition to 0deg (Union)
                start_deg = 140
                if ti < 40: 
                    deg = start_deg
                elif ti < 90:
                    # Transition phase (Surrender)
                    progress = (ti - 40) / 50
                    deg = start_deg * (1 - progress)
                else:
                    deg = 0
                d_theta = np.deg2rad(deg)
            else:
                d_theta = np.deg2rad(90) # Neutral/Indifferent
            
            # 4. Calculate Coupling Force (Mutual Inductance M)
            align = get_alignment_factor(d_theta)
            select = get_selection_gate(sc["compat"])
            
            # M = k * S * A * sqrt(L1*L2)
            M = cfg.coupling_k * np.sqrt(cfg.L1 * cfg.L2) * align * select
            
            # 5. Solve Circuit ODE (Coupled RLC)
            # L1*dI1/dt + R1*I1 + q1/C1 + M*dI2/dt = V1
            det = cfg.L1 * cfg.L2 - M**2
            if det < 1e-6: det = 1e-6 # Avoid singularity
            
            rhs1 = V1 - R_curr * I1 - q1 / cfg.C1
            rhs2 = V2 - R_curr * I2 - q2 / cfg.C2
            
            dI1 = (cfg.L2 * rhs1 - M * rhs2) / det
            dI2 = (-M * rhs1 + cfg.L1 * rhs2) / det
            
            # Update State (Euler integration for simplicity)
            q1 += I1 * cfg.dt
            q2 += I2 * cfg.dt
            I1 += dI1 * cfg.dt
            I2 += dI2 * cfg.dt
            
            # Log
            log_I1[i] = I1
            log_I2[i] = I2
            log_M[i] = M
            log_Align[i] = align
            log_R[i] = R_curr

        results[sc["name"]] = {
            "t": t, "I1": log_I1, "I2": log_I2, 
            "M": log_M, "Align": log_Align, "R": log_R
        }

    plot_results(results)

def plot_results(results):
    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    
    idx = 0
    for name, data in results.items():
        ax_curr = axes[0, idx]
        ax_meta = axes[1, idx]
        t = data["t"]
        
        # Plot Currents (Energy Flow)
        ax_curr.plot(t, data["I1"], label="Person 1 (I1)", color="#00ffff", alpha=0.9)
        ax_curr.plot(t, data["I2"], label="Person 2 (I2)", color="#ff00ff", alpha=0.9)
        ax_curr.set_title(f"{name}: Energy Flow I(t)")
        ax_curr.set_ylabel("Current (Amps/Love)")
        ax_curr.grid(True, alpha=0.3)
        ax_curr.legend(loc="upper left")
        
        # Plot Metadata (Alignment & Coupling)
        ax_meta.plot(t, data["Align"], label="Alignment A (Phase)", color="#ffff00", linestyle="--")
        ax_meta.plot(t, data["M"], label="Mutual Force M", color="#00ff00", linewidth=2)
        ax_meta.set_title("Coupling Dynamics")
        ax_meta.set_ylabel("Force / Alignment")
        ax_meta.set_xlabel("Time (s)")
        ax_meta.grid(True, alpha=0.3)
        ax_meta.legend(loc="upper left")
        
        if idx == 0:
            # Add text annotation for the runner phase
            ax_meta.text(10, -0.6, "RUNNER PHASE\n(Repulsion)", color="red", fontsize=9)
            ax_meta.text(100, 0.6, "UNION\n(Locking)", color="white", fontsize=9, fontweight='bold')
            
        idx += 1

    plt.tight_layout()
    plt.savefig("tye_simulation_results.png")
    print("Simulation complete. Saved to tye_simulation_results.png")

if __name__ == "__main__":
    run_simulation()
