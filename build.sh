#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

make install && python manage.py compilemessages && make collectstatic && make migrate
