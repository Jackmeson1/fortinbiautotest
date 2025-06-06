import unittest

from FortiNBIManager import FortiNBIManager
from ssh_helper import ssh_and_run_command
from testcases.test_block import TestBlock
from testcases.test_isolate import TestBrowserIsolation

if __name__ == "__main__":
    # SSH to a remote host and run a command
    output = ssh_and_run_command("hostname", 22, "username", "password", "your_command")
    print("SSH Output:", output)

    # Check if a process is running and start it if not

    proc = None
    if not FortiNBIManager.is_process_running('FortiNBI.exe'):
        proc = FortiNBIManager.start_process(r'C:\Program Files (x86)\Fortinet\FortiNBI\FortiNBI.exe')


    # Create test suite
    suite = unittest.TestSuite()

    suite.addTest(TestBlock)
    suite.addTest(TestBrowserIsolation)

    # Run the test suite
    unittest.TextTestRunner().run(suite)

    if proc:
        FortiNBIManager.stop_process(proc)
