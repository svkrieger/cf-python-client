from cloudfoundry_client.json_object import JsonObject
from cloudfoundry_client.v3.entities import EntityManager, Entity
from time import sleep
import polling2

class JobFailed(Exception):
    pass

class JobManager(EntityManager):
    def __init__(self, target_endpoint: str, client: 'CloudFoundryClient'):
        super(JobManager, self).__init__(target_endpoint, client, '/v3/jobs')

    def wait_for_job_completion(self, job_guid: str) -> Entity:

        job = polling2.poll(lambda: self.get(job_guid),
            step=1,
            step_function=lambda step: max(step+step,60),
            poll_forever=False,
            timeout=600,
            check_success=lambda job: job['state'] != 'PROCESSING'
            )

        return job
