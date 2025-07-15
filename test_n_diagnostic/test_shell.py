import unittest
from unittest.mock import MagicMock, patch
import io
import sys
import os
from rich.console import Console

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from shell import GLPIExplorerShell

class TestShellInteraction(unittest.TestCase):

    @patch('src.shell.ConfigManager')
    @patch('src.shell.ApiClient')
    @patch('prompt_toolkit.PromptSession.prompt')
    def test_list_computer_command(self, mock_prompt, mock_api_client_class, mock_config_manager_class):
        """
        Tests the 'list computer' command interaction.
        """
        # --- Setup Mocks ---
        # Mock ConfigManager
        mock_config_manager = mock_config_manager_class.return_value
        mock_config_manager.load_config.return_value = {
            'url': 'http://test.glpi/api',
            'app_token': 'test_app_token',
            'user_token': 'test_user_token'
        }

        # Mock ApiClient
        mock_api_client = mock_api_client_class.return_value
        mock_api_client.connect.return_value = True
        mock_api_client.list_items.return_value = [
            {'id': 1, 'name': 'TEST-PC-01', 'states_id': 5},
            {'id': 2, 'name': 'TEST-PC-02', 'states_id': 2},
        ]

        # Mock user input from prompt_toolkit
        mock_prompt.side_effect = [
            'list computer',
            'exit'
        ]

        # --- Capture Console Output ---
        string_io = io.StringIO()
        test_console = Console(file=string_io, force_terminal=True, width=120)

        # --- Run the shell ---
        shell = GLPIExplorerShell(console=test_console)
        shell.run()

        # --- Assertions ---
        # 1. Check if list_items was called correctly
        mock_api_client.list_items.assert_called_once_with('Computer')

        # 2. Check the console output
        output = string_io.getvalue()
        self.assertIn("Liste des Computer", output)
        self.assertIn("TEST-PC-01", output)
        self.assertIn("TEST-PC-02", output)
        self.assertIn("ID", output)
        self.assertIn("Nom", output)
        self.assertIn("Statut", output)

        # 3. Check if session was closed
        mock_api_client.close_session.assert_called_once()

if __name__ == '__main__':
    unittest.main()
