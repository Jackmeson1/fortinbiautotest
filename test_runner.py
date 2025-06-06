import unittest

from FortiNBIManager import FortiNBIManager
from ssh_helper import ssh_and_run_command
from testcases.test_block import TestBlock

from src.utils import read_config
import os


if __name__ == "__main__":
    # SSH to a remote host and run a command

    stdout, stderr = ssh_and_run_command('hostname', 22, 'username', 'password', 'your_command')
    print("SSH Output:", stdout)
    if stderr:
        print("SSH Errors:", stderr)


    # Load configuration
    project_root = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    cfg = read_config(config_path)

    # Check if a process is running and start it if not

    proc = None
    if not FortiNBIManager.is_process_running('FortiNBI.exe'):

        FortiNBIManager.start_process(cfg['fnbi']['executable_path'])


    # Create test suite
    suite = unittest.TestSuite()

    suite.addTest(TestBlock)
    suite.addTest(TestBrowserIsolation)

    # Run the test suite
    unittest.TextTestRunner().run(suite)

    if proc:
        FortiNBIManager.stop_process(proc)
