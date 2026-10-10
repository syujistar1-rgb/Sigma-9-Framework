"""
Sigma-9 Framework Demonstration Script
Runs a simulated streaming telemetry frame through AST guardrails and Bayesian surprisal check.
"""

from sigma9.core import Sigma9CoreEngine

def main():
    print("🚀 Initializing Sigma-9 Multi-Domain Engine...")
    engine = Sigma9CoreEngine()

    # Simulate an incoming astronomical transient alert frame
    sample_event = {
        "snr": 12.4,
        "mag": 15.2,  # Bright transient signal
        "ra": 120.45012,
        "dec": 45.11234
    }

    print(f"📥 Processing incoming telemetry frame: {sample_event}")
    result = engine.process_telemetry_event(sample_event)

    print("\n📊 Sigma-9 Execution Result:")
    for k, v in result.items():
        print(f"  - {k}: {v}")

if __name__ == "__main__":
    main()
