# Project Agents

This repository contains several helper components that act as "agents" for the test suites:

- **BrowserControl** (`src/browser_control.py`)
  - Wraps Selenium WebDriver and provides convenience methods for navigating, checking page state and verifying isolation conditions.
- **FNBIApp** (`src/fnbi_app.py`)
  - Launches and controls the FortiNBI desktop application and its associated isolator.
- **FNBIService** (`src/fnbi_service.py`)
  - Manages the Windows service used by FortiNBI, including start, stop and status checks.
- **FortiNBIManager** (`FortiNBIManager.py`)
  - Performs low-level process management tasks, such as detecting running processes.
- **ssh_helper** (`ssh_helper.py`)
  - Executes remote commands over SSH and returns the output.

These agents are used throughout the tests found in `fnbi_tests/` and `tests/` to automate and verify different FortiNBI features.
