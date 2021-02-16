import sys
import unittest
from http import HTTPStatus
from unittest.mock import patch, mock_open

import cloudfoundry_client.main.main as main
from abstract_test_case import AbstractTestCase
from cloudfoundry_client.v3.entities import Entity, EntityManager

class TestBuildpacks(unittest.TestCase, AbstractTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client_class()

    def setUp(self):
        self.build_client()

    def test_get(self):
        self.client.get.return_value = self.mock_response(
            '/v3/jobs/job_id',
            HTTPStatus.OK,
            None,
            'v3', 'jobs', 'GET_{id}_processing_response.json')
        result = self.client.v3.jobs.get('job_id')
        self.client.get.assert_called_with(self.client.get.return_value.url)
        self.assertIsNotNone(result)

    def test_wait_for_job(self):
        self.client.get.side_effect = [
            self.mock_response(
                '/v3/jobs/job_id',
                HTTPStatus.OK,
                None,
                'v3', 'jobs', 'GET_{id}_processing_response.json'),
            self.mock_response(
                '/v3/jobs/job_id',
                HTTPStatus.OK,
                None,
                'v3', 'jobs', 'GET_{id}_processing_response.json'),
            self.mock_response(
                '/v3/jobs/job_id',
                HTTPStatus.OK,
                None,
                'v3', 'jobs', 'GET_{id}_complete_response.json'),
            ]

        result = self.client.v3.jobs.wait_for_job('job_id')

        assert self.client.get.call_count == 3
        self.assertIsNotNone(result)