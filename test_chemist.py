import chemist
import unittest

class ChemistTest(unittest.TestCase):
    def test_security_validation(self):
        body = b'{"key":"value"}'
        signature = "a4b19954c9b3e8e0ef1b7c993fcff7e2a2564bf6"
        secret = b"token_stored_in_github_webhook_configuration"
        self.assertTrue(chemist.verify_signature(body, signature, secret))
        self.assertFalse(chemist.verify_signature(body, 'plain wrong signature', secret))
