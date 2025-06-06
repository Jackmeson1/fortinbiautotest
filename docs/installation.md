# FortiNBI Automated Testing Installation

## Prerequisites

- Windows 10 or Windows 11
- Python 3.7 or higher
- Git

## Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fnbi-automated-testing.git
   cd fnbi-automated-testing
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install the project in editable mode:
   ```
   pip install -e .
   ```

5. Configure the project:
   - Copy `config/config.yaml.example` to `config/config.yaml`
   - Edit `config/config.yaml` and set the appropriate paths and settings for your environment

## Verifying the Installation

To verify that the installation was successful, run:

```
pytest -v
```

This should run all the tests and show their results.
