"""
Sigma-9 Framework - Quantum Telemetry & Axiomatic State-Space Mapping Module
Enforces density matrix physical invariants and quantum Bures fidelity surprisal.
"""

import math
from typing import Any, Dict, Tuple
import numpy as np


class QuantumAxiomaticGuardrail:
    """Layer 2: Axiomatic State-Space Guardrail enforcing physical quantum invariants
    on single-qubit density matrices derived from Bloch vector components.
    """

    def __init__(self, trace_tol: float = 1e-4, positivity_tol: float = -1e-6):
        self.trace_tol = trace_tol
        self.positivity_tol = positivity_tol

    def pauli_to_density_matrix(self, rx: float, ry: float, rz: float) -> np.ndarray:
        """Constructs a 2x2 density matrix from Bloch vector components <X>, <Y>, <Z>."""
        I = np.eye(2, dtype=complex)
        sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
        sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
        
        rho = 0.5 * (I + rx * sigma_x + ry * sigma_y + rz * sigma_z)
        return rho

    def evaluate(self, payload: Dict[str, Any]) -> Tuple[bool, str]:
        """Validates density matrix against fundamental quantum axioms:
        1. Unit Trace: Tr(rho) = 1
        2. Positive Semi-Definiteness: lambda_min >= 0
        3. Purity Bound: Tr(rho^2) <= 1
        """
        if not all(k in payload for k in ("rx", "ry", "rz")):
            return False, "Missing Bloch vector components (rx, ry, rz)"

        rho = self.pauli_to_density_matrix(payload["rx"], payload["ry"], payload["rz"])

        # Axiom 1: Unit Trace Check
        trace_val = np.real(np.trace(rho))
        if abs(trace_val - 1.0) > self.trace_tol:
            return False, f"Unit Trace Violation: Tr(rho) = {trace_val:.6f} != 1.0"

        # Axiom 2: Positive Semi-Definiteness (Non-negative Eigenvalues)
        eigenvalues = np.linalg.eigvalsh(rho)
        min_eig = np.min(eigenvalues)
        if min_eig < self.positivity_tol:
            return False, f"Unphysical State: Minimum eigenvalue lambda = {min_eig:.6f} < 0"

        # Axiom 3: Purity Bound Tr(rho^2) <= 1.0
        purity = np.real(np.trace(rho @ rho))
        if purity > 1.0 + self.trace_tol:
            return False, f"Purity Violation: Tr(rho^2) = {purity:.6f} > 1.0"

        return True, f"ACCEPTED (Purity = {purity:.4f})"


class QuantumBayesianStateTracker:
    """Layer 3: Quantum Bayesian inference tracking state fidelity and Bures Distance."""

    def __init__(self, target_state_rho: np.ndarray):
        self.target_rho = target_state_rho

    def bures_fidelity(self, rho: np.ndarray) -> float:
        """Computes Quantum State Fidelity F(rho_target, rho)."""
        sqrt_target = self._matrix_sqrt(self.target_rho)
        M = sqrt_target @ rho @ sqrt_target
        sqrt_M = self._matrix_sqrt(M)
        fidelity = np.real(np.trace(sqrt_M)) ** 2
        return float(np.clip(fidelity, 0.0, 1.0))

    def _matrix_sqrt(self, A: np.ndarray) -> np.ndarray:
        vals, vecs = np.linalg.eigh(A)
        vals = np.maximum(vals, 0.0)
        return vecs @ np.diag(np.sqrt(vals)) @ vecs.conj().T

    def compute_quantum_surprisal(self, rho: np.ndarray) -> Tuple[float, float, bool]:
        """Calculates quantum surprisal via Bures Distance metric."""
        fidelity = self.bures_fidelity(rho)
        bures_distance = math.sqrt(max(0.0, 2.0 * (1.0 - math.sqrt(fidelity))))
        surprisal_nats = (bures_distance ** 2) * 10.0
        is_anomaly = surprisal_nats > 5.0
        return float(fidelity), surprisal_nats, is_anomaly
