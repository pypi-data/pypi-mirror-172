class EstimateResult:
    def __init__(self, data):
        self.device = data.get("device")
        self.estimate_ms = data.get("estimate_ms")
        self.num_qubits = data.get("num_qubits")
        self.qc = data.get("qc")
        self.warning_message = data.get("warning_message")
