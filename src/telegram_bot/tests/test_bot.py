import pytest
from unittest.mock import patch, MagicMock
from src.telegram_bot.bot import send_screenshot_with_explanation

@patch('src.telegram_bot.bot.bot')
def test_send_screenshot_with_explanation(mock_bot):
    mock_bot.send_photo = MagicMock()
    send_screenshot_with_explanation('../../sample_data/sample_screenshot.png', '../../sample_data/sample_signal.json')
    mock_bot.send_photo.assert_called()
