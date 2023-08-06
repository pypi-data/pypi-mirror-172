from unittest import SkipTest

import requests

from tests.cli.auth_utils import handle_device_code_flow
from tests.cli.base import CliTestCase


class TestEndToEnd(CliTestCase):
    """ """
    TEST_CONTEXT_URL = 'explorer.alpha.dnastack.com'

    @classmethod
    def setUpClass(cls) -> None:
        if not requests.get(f'https://{cls.TEST_CONTEXT_URL}').ok:
            raise SkipTest(f'The testing server ({cls.TEST_CONTEXT_URL}) is not available for this test.')

        cls.reset_session()
        cls.prepare_for_device_code_flow(email_env_var_name='E2E_STAGING_AUTH_DEVICE_CODE_TEST_EMAIL',
                                         token_env_var_name='E2E_STAGING_AUTH_DEVICE_CODE_TEST_TOKEN')
        handle_device_code_flow(['python', '-m', 'dnastack', 'use', cls.TEST_CONTEXT_URL],
                                cls._states['email'],
                                cls._states['token'])

    def test_182678656(self):
        """
        https://www.pivotaltracker.com/story/show/182678656

        When using the "dnastack collections query" command after initializing with the "dnastack use" command,
        there should not be an additional auth prompt if the target per-collection data-connect endpoint is registered.
        """
        self.invoke('use', self.TEST_CONTEXT_URL)
        self.simple_invoke('collections',
                           'query',
                           '-c', 'explorer-staging-controlled-collection',
                           'SELECT 1')
