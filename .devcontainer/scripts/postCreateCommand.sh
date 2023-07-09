#!/bin/bash
set -o allexport
# # source /workspaces/shoplist/.env
# # source /workspaces/shoplist/app/.env
set +o allexport

cd /workspaces/shoplist/api
poetry install

# cd /workspaces/shoplist/app
# npm install
