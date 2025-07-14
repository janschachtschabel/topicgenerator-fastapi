# topic-tree-generator / Themenbaum-Generator

This project is a fastAPI implementation of Jan Schachtschabel's "Themenbaum-Generator"-idea.

The following Jira issues and Confluence articles are relevant to this project:

- https://edu-sharing.atlassian.net/browse/GEN-101
- https://edu-sharing.atlassian.net/browse/GEN-102
- [KI-Workflow - Themenbaumstruktur mit KI generieren](https://edu-sharing.atlassian.net/wiki/spaces/ESS/pages/971866113/KI-Workflow+-+Themenbaumstruktur+mit+KI+generieren)

## Getting started

This project requires **Python 3.13**.

The dependencies of this project are managed by [uv](https://docs.astral.sh/uv/).
Therefore, before trying to run this project,
please make sure that
you [have installed the most recent version of uv](https://docs.astral.sh/uv/getting-started/installation/).

### Setting up the local development environment in your IDE

To get started, you can run the following commands in your shell (after you have cloned this `git` repository)
**from this project's root directory**:

```shell
# create the virtual environment:
uv venv
# you should now be able to see a .venv directory in your project's root directory.

# install the project dependencies according to the "pyproject.toml"- / "uv.lock"-file:
uv sync
```

#### additional hints

If your system OS does not provide an up-to-date Python version,
you can use `uv`
to [install specific Python versions ](https://docs.astral.sh/uv/guides/install-python/#installing-a-specific-version)
before running the above commands.

PyCharm supports `uv` for package and environment
management [since PyCharm 2024.3.2](https://www.jetbrains.com/pycharm/whatsnew/#page__content-package-management).

After opening the project in PyCharm,
you should be able to see
a [PyCharm fastAPI runConfiguration](https://www.jetbrains.com/help/pycharm/fastapi-project.html) for the `main.py` in
the "run"-view.
*(see also: [PyCharm Run/debug configurations](https://www.jetbrains.com/help/pycharm/fastapi-project.html))*

## Contributing

If you want to contribute to this project, your commits should pass the GitLab CI/CD pipelines.
Merge Requests will automatically display the results of the pipeline run
and give you an overview if the code quality has changed.

Since this project uses [ruff](https://docs.astral.sh/ruff/) for linting and code formatting,
you can run the following commands locally to make sure that your commits pass the pipelines:

```shell
ruff check   # Lint all files in the current directory.
ruff format  # Format all files in the current directory.
```

***