import collections
from io import BytesIO

import numpy as np
import requests
from dateutil.parser import parse


class JobResult:
    def __init__(self, data):
        # "COMPLETED" | "PENDING" | "QUEUED" | "RUNNING"
        self.run_status = data.get("run_status")
        self.queue_time_ms = data.get("queue_time_ms")
        self.run_time_ms = data.get("run_time_ms")
        self.job_id = data.get("job_id")
        self.sv_link = data.get("sv_link")
        self.top_100_results = data.get("top_100_results")
        self.num_qubits = data.get("num_qubits")
        self.qc = data.get("qc")
        self.tags = data.get("tags")

        self.queue_start = data.get("queue_start")
        if self.queue_start is not None:
            self.queue_start = parse(self.queue_start)

        self.queue_end = data.get("queue_end")
        if self.queue_end is not None:
            self.queue_end = parse(self.queue_end)

        self.run_start = data.get("run_start")
        if self.run_start is not None:
            self.run_start = parse(self.run_start)

        self.run_end = data.get("run_end")
        if self.run_end is not None:
            self.run_end = parse(self.run_end)

        Status = collections.namedtuple("Status", ["success", "error_message"])
        self.status = Status(data.get("success"), data.get("error_message"))
        self.worker_runtime_ms = data.get("worker_runtime_ms")

    def get_statevector(self):
        if self.sv_link is not None:
            data = requests.get(self.sv_link, timeout=100).content
            return np.load(BytesIO(data))
        return None
