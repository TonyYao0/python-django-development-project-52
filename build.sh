curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env


make install

uv run python manage.py compilemessages


make collectstatic
make migrate