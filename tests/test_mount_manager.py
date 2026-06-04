import unittest
from unittest.mock import patch, MagicMock
from drivenautilus.mount_manager import MountManager

class TestMountManager(unittest.TestCase):
    def setUp(self):
        self.manager = MountManager("gdrive", "~/GoogleDrive")

    @patch('drivenautilus.command_runner.CommandRunner.run_sync')
    def test_is_mounted(self, mock_run):
        mock_run.return_value.success = True
        self.assertTrue(self.manager.is_mounted())
        
        mock_run.return_value.success = False
        self.assertFalse(self.manager.is_mounted())

if __name__ == '__main__':
    unittest.main()
