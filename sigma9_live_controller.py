import requests
import numpy as np
import time
import sys

def get_live_grid_carbon_intensity():
    """Fetches real-time physical carbon intensity data (gCO2/kWh)"""
    url = "https://carbonintensity.org.uk"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        forecast_carbon = data['data'][0]['intensity']['forecast']
        index_rating = data['data'][0]['intensity']['index']
        return forecast_carbon, index_rating
    except Exception as e:
        print(f"❌ Infrastructure Connection Error: {e}")
        return None, None

def execute_real_cpu_computation(duration_cycles):
    """Executes actual, intensive floating-point matrix operations on your CPU"""
    # This physically exercises your processor cores with raw mathematics
    matrix_size = 500
    for _ in range(duration_cycles):
        A = np.random.rand(matrix_size, matrix_size)
        B = np.random.rand(matrix_size, matrix_size)
        np.dot(A, B) # Real matrix multiplication executing on your silicon hardware

# --- THE OPERATIONAL LIVE CONTROLLER LOOP ---
print("🌍 INITIATING LIVE SIGMA-9 PRODUCTION CONTROLLER...")
print("=========================================================")

# Define our strict operational boundary (grams of CO2 per kilowatt-hour)
CARBON_CEILING_THRESHOLD = 120 

# 1. Fetch real-world planetary energy metrics
carbon_gco2, grid_status = get_live_grid_carbon_intensity()

if carbon_gco2 is not None:
    print(f"📊 LIVE PLANETARY DATA CAPTURED:")
    print(f"Current Grid Emissions: {carbon_gco2} gCO2/kWh")
    print(f"Physical Grid Status:   {grid_status.upper()}")
    print("---------------------------------------------------------")
    
    # 2. Hard Algorithmic Decision Loop based on your standalone theory
    if carbon_gco2 <= CARBON_CEILING_THRESHOLD:
        print("🟢 OPERATIONAL DECISION: GRID ENERGETICS ARE CLEAN")
        print("🚀 System Action: Flipping internal remote control to Hyper-Focus.")
        print("Executing heavy Sigma-9 mathematical arrays at maximum bandwidth...")
        
        start_time = time.time()
        execute_real_cpu_computation(duration_cycles=80) # High computational load
        print(f"✅ Real-world task completed in {time.time() - start_time:.2f} seconds safely.")
        
    else:
        print("🔴 OPERATIONAL DECISION: GRID ENERGETICS ARE DIRTY")
        print("⚠️ System Action: Applying strict temporal throttling constraint.")
        print("Slowing down execution engine loop to protect planetary ecosystem resources...")
        
        start_time = time.time()
        execute_real_cpu_computation(duration_cycles=5) # Minimal computation load to conserve energy
        print(f"🍃 Throttled task completed safely in {time.time() - start_time:.2f} seconds.")

else:
    print("🛑 Critical Error: Unable to sync with live planetary infrastructure data networks.")
    sys.exit(1)

print("=========================================================")
print("🔒 SYSTEM EXECUTION CYCLE COMPLETED GRACEFULLY.")
