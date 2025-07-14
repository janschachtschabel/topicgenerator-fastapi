# see: https://docs.astral.sh/uv/guides/integration/docker/
# and: https://github.com/astral-sh/uv-docker-example

# Use a Python Image that comes with uv pre-installed:
FROM ghcr.io/astral-sh/uv:python3.13-bookworm

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

# use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []

# Run the FastAPI application by default
# Uses `fastapi dev` to enable hot-reloading when the `watch` sync occurs
# Uses `--host 0.0.0.0` to allow access from outside the container
#CMD ["fastapi", "dev", "--host", "0.0.0.0", "app/main.py"]

# see: https://fastapi.tiangolo.com/deployment/docker/#dockerfile
# Run the FastAPI application without hot-reloading:
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0" ,"--port", "80"]