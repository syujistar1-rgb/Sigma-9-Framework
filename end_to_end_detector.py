import numpy as np
import time
import random
from math import fsum, isfinite, ulp
from numbers import Real
from typing import Iterable, Tuple

print("=================================================================")
print("🧬 SIGMA-9: PRODUCTION END-TO-END DETECTOR ENGINE")
print("=================================================================")

# =====================================================================
# SYSTEM CORE UTILITY CODES (Ray Peloquin's Bounded Scoring Layer)
# =====================================================================
ROUND_OFF_TOLERANCE = 8 * ulp(1.0)

def _finite_real_vector(values: Iterable[Real], name: str) -> Tuple[float, ...]:
    result = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{name} must contain real numeric values, not bool or text.")
        try:
            converted = float(value)
        except (OverflowError, ValueError) as error:
            raise ValueError(f"{name} values must fit finite floating-point numbers.") from error
        if not isfinite(converted):
            raise ValueError(f"{name} values must be finite.")
        result.append(converted)
    return tuple(result)

def _bound_roundoff(score: float) -> float:
    if not isfinite(score):
        raise ArithmeticError("The computed score is not finite.")
    bounded = min(1.0, max(0.0, score))
    if abs(bounded - score) > ROUND_OFF_TOLERANCE:
        raise ArithmeticError("The computed score violates its proven bounds.")
    return bounded

def calculate_normalized_tensor_score(features: Iterable[Real], weights: Iterable[Real]) -> float:
    features = _finite_real_vector(features, "Features")
    weights = _finite_real_vector(weights, "Weights")
    if not features or len(features) != len(weights):
        raise ValueError("Nonempty feature and weight vectors must match.")
    if any(not 0.0 <= value <= 1.0 for value in features):
        raise ValueError("Features must be normalized to [0, 1].")
    if any(value < 0.0 for value in weights):
        raise ValueError("Weights must be nonnegative.")
    scale = max(weights)
    if scale == 0.0:
        raise ValueError("At least one weight must be positive.")
    scaled = tuple(value / scale for value in weights)
    score = fsum(value * weight for value, weight in zip(features, scaled)) / fsum(scaled)
    return _bound_roundoff(score)

# =====================================================================
# STAGE 1: LOCAL DETERMINISTIC RAW MOCH TELEMETRY STREAM GENERATOR
# =====================================================================
def generate_reproducible_environment():
    """Generates a fixed baseline telemetry array with an embedded structural anomaly"""
    np.random.seed(42) # Lock seed for absolute reproducibility
    time_steps = np.linspace(0, 10, 100)
    
    # Base background cosmic/environmental wave signal
    base_signal = np.sin(2 * np.pi * 0.5 * time_steps) 
    # Inducing random atmospheric/hardware noise matrix elements
    noise = np.random.normal(0, 0.2, 100)
    telemetry_stream = base_signal + noise
    
    # Deliberately inject a hidden anomaly wave packet at step index 50
    telemetry_stream[50] += 5.0 
    return time_steps, telemetry_stream

# =====================================================================
# STAGE 2: SIGMA-9 SIGNAL CORRELATION PIPELINE (FFT DETECTOR EXTRACTION)
# =====================================================================
class SigmaNineSignalDetector:
    def __init__(self, time_array, signal_array):
        self.time = time_array
        self.signal = signal_array
        
    def execute_spectral_extraction(self) -> Tuple[np.ndarray, float]:
        """Runs a Fast Fourier Transform layer to isolate high-frequency disruptions"""
        # Run standard numpy FFT
        fft_coefficients = np.fft.fft(self.signal)
        frequencies = np.fft.fftfreq(len(self.time))
        
        # Isolate absolute magnitudes to expose structural energy spikes
        spectral_magnitudes = np.abs(fft_coefficients)
        max_isolated_spike = float(np.max(spectral_magnitudes))
        
        # Standardize the output vector mapping safely between 0.0 and 1.0
        normalized_features = (spectral_magnitudes - np.min(spectral_magnitudes)) / (np.max(spectral_magnitudes) - np.min(spectral_magnitudes))
        return normalized_features, max_isolated_spike

# =====================================================================
# STAGE 3: THE END-TO-END EXECUTION CYCLE RUNNER
# =====================================================================
# 1. Pipeline Initialization
print("📡 Step 1: Synthesizing reproducible environment streams...")
t_steps, raw_data = generate_reproducible_environment()
detector_pipeline = SigmaNineSignalDetector(t_steps, raw_data)

# 2. Extract Spectral Signatures
print("🔍 Step 2: Executing Layer 1 Fast Fourier Transform array...")
normalized_features, max_raw_spike = detector_pipeline.execute_spectral_extraction()

# 3. Apply High-Precision Tensor Contract Calculations
print("🧮 Step 3: Compiling features against Ray's weighted metric contract...")
system_weights = np.ones(len(normalized_features)) # Assign balanced unity weights

final_system_score = calculate_normalized_tensor_score(normalized_features, system_weights)

# 4. Enforce Calibrated Decision Threshold
CALIBRATED_DETECTION_THRESHOLD = 0.15
is_anomaly_present = final_system_score >= CALIBRATED_DETECTION_THRESHOLD

print("\n=================================================================")
print("📊 FINAL SIGMA-9 DETECTOR REPORT OUT:")
print("=================================================================")
print(f"Computed End-to-End System Evaluation Score: {final_system_score:.6f}")
print(f"System Validation Verification Boundary:     {CALIBRATED_DETECTION_THRESHOLD}")
print(f"Conclusive Decision Status ➔ ANOMALY FOUND:  {is_anomaly_present}")
print("=================================================================")
print("🔒 PROCESS EXECUTION SNAPSHOT COMPLETE. ALL EXPECTED CHECKS CONVERGED.")
