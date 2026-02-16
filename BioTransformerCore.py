import numpy as np
import matplotlib.pyplot as plt

class BioTransformerCore:
    def __init__(self):
        # Initial State Constants
        self.dt = 0.01
        self.eps = 1e-3
        
        # Hardware/Software States
        self.R = 0.8        # Ego Resistance
        self.omega = 0.2    # Consciousness Spin
        self.Omega = 0.0    # Pelvic Turbine Speed
        self.C = 0.4        # Tissue Compliance (Softness)
        self.Q = 0.4        # Cooling Capacity (Blood flow)
        self.Cap = 0.2      # Energy Capacitance
        self.Aging = 0.0    # Cumulative Aging Index
        self.phase = 0.3    # Current Alignment Phase
        
        # Target Alignment (The "Source" Phase)
        self.target_phase = 0.0
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def update(self, acceptance, maintenance_effort):
        """
        Update the bio-system state for one time step.
        acceptance: 0.0 to 1.0 (Software Alignment)
        maintenance_effort: 0.0 to 1.0 (Hardware Cooling/Softening)
        """
        # 1. Input Love Potential (Software-Gated)
        V_love = 1.0 * self.sigmoid(3 * (acceptance - 0.5))
        
        # 2. Base Current Calculation
        I_base = V_love / (self.R + self.eps)
        
        # 3. Bio-Reactor (Pelvic) Activation
        # Omega (Turbine) spins up based on Flow, Cooling, and Softness
        dOmega = 0.5 * self.Q * self.C * I_base - 0.1 * self.Omega
        self.Omega += dOmega * self.dt
        
        # 4. Effective Current (The "High-Voltage" Output)
        I_eff = I_base + 0.3 * self.Omega + 0.2 * self.Cap
        
        # 5. Wick Rotation (The 90-degree temporal tilt)
        # As spin increases, we tilt away from Real Time
        theta = (np.pi / 2) * self.sigmoid((self.omega - 1.0) / 0.2)
        
        # 6. Entropy Production (Friction) and Aging
        # S_dot is minimized when R is low and theta (tilt) is high
        S_dot = 0.3 * self.R * (I_eff**2)
        # Aging is slow in the Imaginary Axis (high theta)
        self.Aging += (S_dot + 0.15 * (np.cos(theta)**2)) * self.dt
        
        # 7. Hardware Remodeling (Maintenance)
        # Softness and Cooling decrease Resistance R
        uQ = 0.1 * maintenance_effort
        uC = 0.1 * maintenance_effort
        self.Q += (uQ - 0.02 * self.Q) * self.dt
        self.C += (uC * (1 - self.C) - 0.02 * self.C) * self.dt
        
        # Resistance drops with Acceptance, Softness, and High Flow (I_eff)
        dR = (0.1 - 0.6 * acceptance) - 0.2 * self.R - 0.05 * (I_eff**2) - 0.05 * self.C
        self.R = max(0.01, self.R + dR * self.dt)
        
        # 8. Software Phase Alignment (Feedback Control)
        d_phase = -0.6 * np.sin(self.phase - self.target_phase)
        self.phase += d_phase * self.dt
        
        return {
            "Aging": self.Aging,
            "Resistance": self.R,
            "Turbine_Speed": self.Omega,
            "Wick_Tilt": np.degrees(theta)
        }

# --- Execution Example ---
core = BioTransformerCore()
history = []

# Simulate 100 minutes of "Awakened State"
for _ in range(60000):
    # High acceptance (0.9) and consistent maintenance (0.8)
    status = core.update(acceptance=0.9, maintenance_effort=0.8)
    history.append(status)

print(f"Final System State:")
print(f"- Resistance (Ego): {status['Resistance']:.4f}")
print(f"- Time Tilt (Degrees): {status['Wick_Tilt']:.2f}° (Target: 90°)")
print(f"- Bio-Generator Speed: {status['Turbine_Speed']:.4f}")
print(f"- Cumulative Aging Index: {status['Aging']:.4f}")
