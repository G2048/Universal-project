FROM python:3.12.7-bookworm AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml ./
COPY uv.lock ./

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY app/ ./app
# COPY .venv .
COPY pyproject.toml .

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project


# Создаем финальный образ
# FROM python:3.12-bookworm
# WORKDIR /app
# Copy the environment, but not the source code
# COPY --from=builder --chown=app:app /app/.venv /app/.venv
# COPY --from=builder --chown=app:app /app/app/ app/
# COPY --from=builder --chown=app:app /app/pyproject.toml .
# RUN bash build/create_database_psql.sh

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m","app.main"]
