from .api import jobs
from .backend_connection import BackendConnection
from .estimate_result import EstimateResult
from .job_result import JobResult


class DeqartClient:
    def __init__(self, api_token=None, config_location=None):
        self._backend_connection = BackendConnection(api_token, config_location)

    def search(self, run_status=None, limit=100, created_later_than=None):
        job_results = jobs.search_jobs(
            self._backend_connection, run_status, limit, created_later_than
        )
        return [
            JobResult(dict(zip(job_results["column_names"], r)))
            for r in job_results["data"]
        ]

    def estimate(self, circuit):
        return EstimateResult(
            jobs.estimate_job_runtime(self._backend_connection, circuit)
        )

    def run(self, circuit, asynchronous=False, debug_size=None):
        submitted_job = jobs.submit_job(self._backend_connection, circuit, debug_size)
        if not asynchronous:
            return self.wait(submitted_job["job_id"])
        return JobResult(submitted_job)

    def wait(self, job_id):
        return JobResult(jobs.wait_for_job(self._backend_connection, job_id))
