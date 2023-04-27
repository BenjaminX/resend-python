import unittest
from unittest.mock import MagicMock, patch

import pytest

from resend import Resend
from resend.exceptions import MissingRequiredFieldsError


class TestResend(unittest.TestCase):
    def test_invalid_api_key(self):
        with pytest.raises(ValueError):
            Resend(api_key="")

    def test_invalid_send_email_args(self):
        with pytest.raises(ValueError):
            client = Resend(api_key="kl_123")
            client.send_email(
                sender="",
                to="to@email.com",
                text="text",
                subject="subj",
            )

        with pytest.raises(ValueError):
            client = Resend(api_key="kl_123")
            client.send_email(
                sender="from@email.com",
                to="",
                text="text",
                subject="subj",
            )

        with pytest.raises(ValueError):
            client = Resend(api_key="kl_123")
            client.send_email(
                sender="from@email.com",
                to="to@email.com",
                subject="",
                text="text",
            )

    def test_request_missing_fields(self):
        patcher = patch("resend.Resend._make_request")
        mock = patcher.start()
        mock.status_code = 422
        m = MagicMock()
        m.status_code = 422

        def mock_json():
            return {
                "statusCode": "422",
                "name": "missing_required_fields",
                "message": "missing field",
            }

        m.json = mock_json
        mock.return_value = m

        with pytest.raises(MissingRequiredFieldsError) as e:
            client = Resend(api_key="kl_123")
            client.send_email(
                to="to@email.com",
                sender="from@email.com",
                subject="subject",
                html="html",
            )
        assert e.type is MissingRequiredFieldsError
        patcher.stop()
