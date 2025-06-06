# FortiNBI Automated Testing

This project contains automated tests for the FortiNBI application.

## Project Structure

The repository is organised into the following top-level directories:

- `src/` – Core helper modules such as `BrowserControl`, `FNBIApp` and `FNBIService`
- `fnbi_tests/` – Automated test suites grouped by feature area
- `tests/` – Unit tests for the helper modules
- `config/` – YAML configuration files
- `resources/` – Baseline images and other static assets
- `mocks/` – Mock web pages and a simple HTTP server used during testing
- `scripts/` – Helper scripts for running and managing tests
- `docs/` – Additional project documentation
- `test_scenarios/` and `testcases/` – YAML files describing manual and automated scenarios

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix or MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

5. Copy `config/config.yaml.example` to `config/config.yaml` and edit the paths for your environment


## Running Tests

Start the mock HTTP server before executing the tests:

```bash
python mocks/simple_http_server.py &
```

To run all tests:

```
pytest fnbi_tests
```

To run tests for a specific module:

```
pytest fnbi_tests/extension
```

## Documentation

- For installation instructions, see [docs/installation.md](docs/installation.md)
- For usage guidelines, see [docs/usage.md](docs/usage.md)

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
