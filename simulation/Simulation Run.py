# --- 3. Run Simulation ---
np.random.seed(42) # Fixed seed for reproducibility
n_days = 200
cfg = PhysicsConfig()
kernel = LoveOSKernel(cfg)

history = {
    't': [], 'x': [], 'y': [], 'A_acc': [], 
    'm': [], 'kappa': [], 'M_flow': [], 'M_stock': []
}
M_total = 0.0

print("--- Simulation Start: The Path to Awakening ---")

for t in range(n_days):
    # Scenario: The "Dark Night of the Soul" -> "Surrender" -> "Flow"
    
    # x (Action): Consistent hard work throughout
    x_t = np.random.normal(5, 1)
    
    # y (Intent): 
    # Days 0-100: Doubt, Fear, Ego-driven (Low y)
    # Days 100+:  Surrender, Prayer, Love-driven (High y)
    if t < 100:
        y_t = np.random.normal(0.2, 0.1) # Noise/Doubt
    else:
        y_t = np.random.normal(0.9, 0.05) # Pure Intent
        
    y_t = np.clip(y_t, 0, 1) 
    
    # Execute Kernel
    a_t, A_acc, m, kappa, dM = kernel.step(x_t, y_t)
    M_total += dM
    
    # Log Data
    history['t'].append(t)
    history['x'].append(x_t)
    history['y'].append(y_t)
    history['A_acc'].append(A_acc)
    history['m'].append(m)
    history['kappa'].append(kappa)
    history['M_flow'].append(dM)
    history['M_stock'].append(M_total)

print("Simulation Complete.")
