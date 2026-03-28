#!/usr/bin/env bash
curl -LsSf https://astral.sh | sh
source $HOME/.local/bin/env

make install && make collectstatic && make migrate
