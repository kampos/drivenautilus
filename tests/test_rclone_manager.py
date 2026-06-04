import unittest
from unittest.mock import patch, MagicMock
from drivenautilus.rclone_manager import RcloneManager

class TestRcloneManager(unittest.TestCase):
    def setUp(self):
        self.manager = RcloneManager("test_drive")

    @patch('drivenautilus.command_runner.CommandRunner.run_sync')
    def test_list_remotes(self, mock_run):
        mock_run.return_value.success = True
        mock_run.return_value.stdout = "drive:\ngdrive:\n"
        
        remotes = self.manager.list_remotes()
        self.assertEqual(remotes, ["drive", "gdrive"])

    @patch('drivenautilus.command_runner.CommandRunner.run_sync')
    def test_remote_exists(self, mock_run):
        mock_run.return_value.success = True
        mock_run.return_value.stdout = "gdrive:\n"
        
        self.manager.remote_name = "gdrive"
        self.assertTrue(self.manager.remote_exists())
        
        self.manager.remote_name = "other"
        self.assertFalse(self.manager.remote_exists())

if __name__ == '__main__':
    unittest.main()
