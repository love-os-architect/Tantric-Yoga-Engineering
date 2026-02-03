# ---------------------------------------------------------
# Tantra Engineering: Reality Manifestation Simulator
# ---------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Style Settings for Professional Publication ---
sns.set_style("darkgrid", {"axes.facecolor": ".92"})
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 12

# --- 2. The Physics Engine ---
# Equation: d_phi/dt = ω0 + κ1*|y| - γ*R + noise
def simulate_phase_trajectory(y_amp, resistance, steps=800, dt=0.01):
    # Universal Constants
    OMEGA_0 = 0.3    # Natural Flow
    KAPPA_1 = 1.8    # Intent Efficiency
    GAMMA   = 2.5    # Resistance Factor (Brake)
    NOISE_STD = 0.2  # Quantum Fluctuations
    PHI_CRITICAL = 6.0 # Reality Threshold (2*pi approx)

    phi = 0.0
    trajectory = [phi]
    time = [0.0]
    hit_index = None
    
    for i in range(1, steps):
        # The Equation of Motion
        drift = (OMEGA_0 + KAPPA_1 * y_amp - GAMMA * resistance)
        # Stochastic Term
        diffusion = np.random.normal(0, NOISE_STD * np.sqrt(dt))
        
        d_phi = drift * dt + diffusion
        phi += d_phi
        
        t_current = i * dt
        time.append(t_current)
        trajectory.append(phi)
        
        # Check for Manifestation
        if hit_index is None and phi >= PHI_CRITICAL:
            hit_index = i

    return np.array(time), np.array(trajectory), hit_index

# --- 3. Scenario Setup ---
scenarios = [
    # A: The Awakened (Superconducting State)
    {"name": "A: The Awakened (High Intent / Zero Resistance)", 
     "y": 2.5, "R": 0.0, "color": "#FF0055", "ls": "-"}, 
    # B: The Seeker (High Friction State)
    {"name": "B: The Seeker (High Intent / High Resistance)",   
     "y": 2.5, "R": 1.75, "color": "#0066FF", "ls": "-"},
    # C: The Sleeper (Drift State)
    {"name": "C: The Sleeper (Low Intent / Low Resistance)",   
     "y": 0.5, "R": 0.5, "color": "#888888", "ls": "--"},
]

# --- 4. Execution & Rendering ---
plt.figure(dpi=150)

for sc in scenarios:
    t, traj, hit_idx = simulate_phase_trajectory(sc["y"], sc["R"])
    
    # Plot Trajectory
    plt.plot(t, traj, label=sc["name"], color=sc["color"], 
             linestyle=sc["ls"], linewidth=2.5, alpha=0.9)
    
    # Mark the "Miracle" moment
    if hit_idx:
        plt.scatter(t[hit_idx], traj[hit_idx], color=sc["color"], s=100, zorder=5, edgecolors='white')
        plt.text(t[hit_idx]-0.6, traj[hit_idx]+0.3, "Phase Shift!", 
                 color=sc["color"], fontweight='bold', fontsize=10)

# --- 5. Annotations ---
# Reality Threshold
plt.axhline(y=6.0, color='#FFD700', linestyle=':', linewidth=3)
plt.text(0.1, 6.1, "REALITY THRESHOLD (Manifestation Zone)", 
         color='#C5A000', fontweight='bold', fontsize=11)
plt.fill_between([0, 8], 6.0, 8.0, color='#FFD700', alpha=0.1)

# Titles and Labels
plt.title("The Physics of Manifestation: Phase Velocity Simulation\n$\\dot{\\phi} = \\kappa |y| - \\gamma R$", 
          fontsize=14, pad=15, fontweight='bold')
plt.xlabel("Physical Time (Delay)", fontsize=11)
plt.ylabel("Accumulated Phase (Meaning)", fontsize=11)
plt.xlim(0, 8)
plt.ylim(0, 7.5)
plt.legend(loc='upper left', framealpha=0.95, fontsize=10)

# Save and Show
plt.tight_layout()
plt.savefig("manifestation_physics_en.png")
plt.show()

print("Graph generated: manifestation_physics_en.png")
