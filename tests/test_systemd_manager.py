import unittest
from unittest.mock import patch, MagicMock
from drivenautilus.systemd_manager import SystemdManager

class TestSystemdManager(unittest.TestCase):
    def setUp(self):
        self.manager = SystemdManager("test.service")

    @patch('drivenautilus.command_runner.CommandRunner.run_sync')
    def test_is_service_enabled(self, mock_run):
        mock_run.return_value.stdout = "enabled\n"
        self.assertTrue(self.manager.is_service_enabled())
        
        mock_run.return_value.stdout = "disabled\n"
        self.assertFalse(self.manager.is_service_enabled())

if __name__ == '__main__':
    unittest.main()
