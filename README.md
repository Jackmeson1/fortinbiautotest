# FortiNBI Automated Testing

This project contains automated tests for the FortiNBI application.

## Project Structure

- `src/`: Contains utility modules for interacting with FNBI components
- `fnbi_tests/`: Contains all automated test modules
- `config/`: Contains configuration files
- `docs/`: Contains project documentation
- `scripts/`: Contains utility scripts for running tests and setting up the environment

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix or MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `config/config.yaml.example` to `config/config.yaml` and edit the paths for your environment

## Running Tests

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

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
