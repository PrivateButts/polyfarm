setup:
    uv sync --dev
    uv run pre-commit install
    cp -n ./example.env ./.env
    just manage collectstatic --noinput
    just manage migrate

test:
    just run pytest

dev:
    just manage runserver

format:
    just run pre-commit run --all-files

format-fix:
    just run pre-commit run black --all-files
    just run ruff check --fix .

run *COMMAND:
    cd src && uv run {{COMMAND}}

manage *COMMAND:
    just run python manage.py {{COMMAND}}

docker *COMMAND:
    docker compose -f docker-compose.yml {{COMMAND}}

docker-dev *COMMAND:
    docker compose -f docker-compose.dev.yml {{COMMAND}}

docker-dev-manage *COMMAND:
    just docker-dev run --rm web python manage.py {{COMMAND}}
