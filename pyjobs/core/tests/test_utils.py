from unittest.mock import patch

from django.test import TestCase, override_settings
from telegram import TelegramError

from pyjobs.core.utils import post_telegram_channel


class TelegramPosterTest(TestCase):
    def setUp(self):
        self.message = "Hello, World!"

    @override_settings(TELEGRAM_TOKEN="my-token")
    @override_settings(TELEGRAM_CHATID="my-channel")
    @patch("pyjobs.core.utils.Bot")
    def test_post_message_to_telegram_successfully(self, mocked_bot):
        result, message = post_telegram_channel(self.message)
        self.assertTrue(result)
        self.assertEqual(message, "success")
        mocked_bot.assert_called_with("my-token")
        mocked_bot.return_value.send_message.assert_called_with(
            chat_id="my-channel", text=self.message
        )

    @override_settings(TELEGRAM_TOKEN=None)
    @override_settings(TELEGRAM_CHATID=None)
    @patch("pyjobs.core.utils.Bot")
    def test_post_no_auth_telegram_channel(self, mocked_bot):
        result, message = post_telegram_channel(self.message)
        self.assertFalse(result)
        self.assertEqual(message, "missing_auth_keys")

    @override_settings(TELEGRAM_TOKEN="my-token")
    @override_settings(TELEGRAM_CHATID="my-channel")
    @patch("pyjobs.core.utils.Bot")
    def test_post_wrong_auth_telegram_channel(self, mocked_bot):
        mocked_bot.return_value.send_message.side_effect = TelegramError("error")
        result, message = post_telegram_channel(self.message)
        self.assertFalse(result)
        self.assertEqual(message, "wrong_auth_keys")
        mocked_bot.assert_called_once_with("my-token")
        mocked_bot.return_value.send_message.assert_called_with(
            chat_id="my-channel", text=self.message
        )
