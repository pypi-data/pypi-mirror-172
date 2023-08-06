# Cerebrium

Cerebrium is the Python package built for use with the [Cerebrium](https://www.cerebrium.ai/) platform, which allows you to deploy your machine learning models as a REST API with a single line of code.

For usage consult the [documentation](https://docs.cerebrium.ai/). The repo for the documentation can be found [here](https://github.com/CerebriumAI/docs).

# Development environment
Cerebrium uses Poetry for dependency management and packaging. To install Poetry, follow the instructions [here](https://python-poetry.org/docs/#installation). Alternatively, consult our article on [how to manage your python environments](https://blog.cerebrium.ai/setting-up-your-data-science-and-ml-development-environment-949277339939?gi=54b980dd4e1d).

You can run the following steps to setup your Python development environment with the following commands:
```bash
poetry install
poetry shell
```
You should use this environment to run tests, notebooks and build the package.

Furthermore, you should set up a `.env` file in the project root with the following environment variables:
```bash
DEVELOPMENT_ENV=dev
```
