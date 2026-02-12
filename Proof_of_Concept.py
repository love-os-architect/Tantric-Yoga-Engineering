import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# Love-OS Core Physics Engine (Ver. 1.0)
# ==========================================

def simulate_love_os(
    steps=200,          # Time duration
    dt=0.1,             # Time step
    initial_dist=1.0,   # Initial separation (normalized)
    
    # Physics Constants
    k=0.5,              # Binding Force Constant (Unconditional Love)
    omega=1.5,          # Rotation/Context Shift (The Spiral Factor)
    
    # Tuning Parameters (The "Human" Factor)
    # Scenario A: Both struggling (Low tuning speed)
    # Scenario B: You represent Superconductivity (High tuning speed)
    scenario='A' 
):
    # Initialize State Vectors
    # d = [x, y] distance vector
    d = np.array([initial_dist, 0.0]) 
    
    # Resistance (Ego)
    # R1 = You, R2 = Partner
    R1, R2 = 0.5, 0.5 
    R_min, R_max = 0.1, 0.8
    
    # Tuning Level (Consciousness)
    # T approaches 1.0 (Enlightenment)
    T1, T2 = 0.0, 0.0 
    
    # Tuning Speed (How fast one surrenders)
    if scenario == 'A': # Normal Relationship
        eta1, eta2 = 0.05, 0.05
    elif scenario == 'B': # Love-OS Practitioner (You are fast)
        eta1, eta2 = 0.5, 0.05 # You are 10x faster at tuning
    else: # No Rotation (Linear logic)
        eta1, eta2 = 0.05, 0.05
        omega = 0.0

    # Data logging
    history = {'t': [], 'd_mag': [], 'Heat': [], 'R1': [], 'R2': [], 'd_vec': []}
    
    for t in np.arange(0, steps * dt, dt):
        # 1. Calculate Binding Force (Love increases as distance decreases)
        dist_mag = np.linalg.norm(d)
        A_eff = k * (1 + 1/(0.1 + dist_mag)) # Force amplifies near center
        
        # 2. Calculate Joule Heat (Suffering)
        # J = I^2 * R (Energy flow squared * Total Resistance)
        # Current I is proportional to Binding Force * Distance
        Current = A_eff * dist_mag
        J = Current**2 * (R1 + R2)
        
        # 3. Update Tuning (Spirituality)
        # Heat (Pain) reduces tuning temporarily (Panic), 
        # but Practice (eta) restores it.
        dT1 = eta1 * (1.0 - T1) - 0.01 * J 
        dT2 = eta2 * (1.0 - T2) - 0.01 * J
        T1 += dT1 * dt
        T2 += dT2 * dt
        
        # Clip T to [0, 1]
        T1 = np.clip(T1, 0, 1)
        T2 = np.clip(T2, 0, 1)
        
        # 4. Update Resistance (Ego)
        # Higher Tuning = Lower Resistance
        R1 = R_min + (R_max - R_min) / (1 + 5 * T1)
        R2 = R_min + (R_max - R_min) / (1 + 5 * T2)
        
        # 5. Motion Dynamics (The Spiral)
        # Convergence Force (-lambda) + Rotation Force (omega)
        lambda_val = 2 * k * A_eff
        
        # Rotation Matrix (90 degrees)
        rot_d = np.array([-d[1], d[0]])
        
        if scenario == 'C': # No rotation
            dd = -lambda_val * d 
        else:
            dd = -lambda_val * d + omega * rot_d
            
        d += dd * dt * 0.05 # Scale for stability
        
        # Log data
        history['t'].append(t)
        history['d_mag'].append(dist_mag)
        history['Heat'].append(J)
        history['R1'].append(R1)
        history['R2'].append(R2)
        history['d_vec'].append(d.copy())
        
    return history

# (Plotting code omitted for brevity, but this logic generates the proofs)
