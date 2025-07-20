import unittest
from unittest.mock import MagicMock, patch
import io
import sys
import os
from rich.console import Console

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.shell import GLPIExplorerShell

class TestShellInteraction(unittest.TestCase):

    @patch('src.shell.TopologyCache.load_from_disk')
    @patch('src.shell.ConfigManager')
    @patch('src.shell.ApiClient')
    @patch('prompt_toolkit.PromptSession.prompt')
    def test_list_computer_command(self, mock_prompt, mock_api_client_class, mock_config_manager_class, mock_load_from_disk):
        """
        Tests the 'list computer' command interaction.
        """
        # --- Setup Mocks ---
        # Force a cache miss to trigger the refresh logic
        mock_load_from_disk.return_value = None

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
        
        # Mock the API calls made during the cache refresh
        def list_items_side_effect(itemtype, item_range="0-9999", only_id=True):
            if itemtype == 'Computer':
                return [{'id': 1}, {'id': 2}]
            return []

        def get_item_details_side_effect(itemtype, item_id):
            if itemtype == 'Computer' and item_id == 1:
                return {'id': 1, 'name': 'TEST-PC-01', 'states_id': 5, 'itemtype': 'Computer'}
            if itemtype == 'Computer' and item_id == 2:
                return {'id': 2, 'name': 'TEST-PC-02', 'states_id': 2, 'itemtype': 'Computer'}
            return {}

        mock_api_client.list_items.side_effect = list_items_side_effect
        mock_api_client.get_item_details.side_effect = get_item_details_side_effect

        # Mock user input from prompt_toolkit
        mock_prompt.side_effect = [
            'list computer',
            'exit'
        ]

        # --- Capture Console Output ---
        # The test runner captures stdout, which is where the shell's Console prints.
        # We can retrieve it later.
        string_io = io.StringIO()
        
        # --- Run the shell ---
        shell = GLPIExplorerShell()
        # We need to redirect the shell's console to capture its output
        shell.console = Console(file=string_io, force_terminal=True, width=120)
        shell.run()

        # --- Assertions ---
        # 1. Check if list_items was called for 'Computer' during the initial refresh
        mock_api_client.list_items.assert_any_call('Computer', item_range="0-9999", only_id=True)

        # 2. Check the console output
        output = string_io.getvalue()
        self.assertIn("TEST-PC-01", output)
        self.assertIn("TEST-PC-02", output)

        # 3. Check if session was closed
        mock_api_client.close_session.assert_called_once()

if __name__ == '__main__':
    unittest.main()
