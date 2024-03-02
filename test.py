import unittest
from unittest.mock import patch, MagicMock
from telegram import start

class TestTelegramBot(unittest.TestCase):
    @patch('telegram.bot')
    @patch('telegram.types')
    def test_start(self, mock_types, mock_bot):
        # Mocking the message and chat objects
        mock_message = MagicMock()
        mock_message.chat.id = 12345

        # Mocking the KeyboardButton and ReplyKeyboardMarkup
        mock_button = MagicMock()
        mock_markup = MagicMock()

        mock_types.KeyboardButton.return_value = mock_button
        mock_types.ReplyKeyboardMarkup.return_value = mock_markup

        # Call the start function
        start(mock_message)

        # Assertions to check if the functions were called correctly
        mock_types.KeyboardButton.assert_called_once_with("a")
        mock_markup.add.assert_called_once_with(mock_button)
        mock_bot.send_message.assert_called_once_with(
            12345, "Выбери юнит:", reply_markup=mock_markup, parse_mode='html'
        )

if __name__ == '__main__':
    unittest.main()