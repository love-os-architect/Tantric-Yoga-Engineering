import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass

# --- 1. Physics Configuration ---
@dataclass
class PhysicsConfig:
    # Integration Parameters
    alpha: float = 1.0       # Weight of Pure Intent (y) - The "Being"
    beta: float  = 0.5       # Weight of Action (x*y) - The "Doing"
    dt: float    = 1.0       # Time step
    
    # Phase Transition Parameters (The Tantra Logic)
    critical_area: float = 80.0   # The Threshold (Ac) required for Awakening
    base_kappa: float    = 100.0  # Exchange Rate BEFORE Awakening (Linear World)
    awakened_kappa: float= 5000.0 # Exchange Rate AFTER Awakening (Superconducting World)
    
    # Hysteresis / Inertia
    transition_speed: float = 0.1 # How fast the reality shifts once triggered
