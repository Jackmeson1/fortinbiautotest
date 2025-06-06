# FortiNBI Automated Testing Usage Guide

## Running Tests

To run all tests:

```
pytest
```

To run tests for a specific module:

```
pytest fnbi_tests/extension
```

To run a specific test:

```
pytest fnbi_tests/extension/test_installation.py::test_extension_installation
```

## Configuration

The project uses a configuration file located at `config/config.yaml`. You can modify this file to change test parameters, paths, and other settings.

## Adding New Tests

To add a new test:

1. Create a new test file in the appropriate subdirectory of `fnbi_tests/`
2. Write your test functions, using the existing tests as examples
3. Use fixtures defined in `conftest.py` as needed
4. Run your new tests to ensure they work as expected

## Generating Test Reports

To generate an HTML test report:

```
pytest --html=report.html
```

## Troubleshooting

If you encounter issues:

1. Ensure all prerequisites are installed
2. Check that the FortiNBI application is properly installed on your system
3. Verify that the paths in `config/config.yaml` are correct
4. Check the logs in `logs/` for any error messages

For further assistance, please open an issue on the GitHub repository.
