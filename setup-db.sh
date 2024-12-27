#!/bin/bash

# Exit on error
set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RESET='\033[0m'

PROJECT_NAME=$(basename "$(dirname "$(dirname "$(realpath "$0")")")")
PROJECT_PATH=$(dirname "$(dirname "$(realpath "$0")")")
DB_USER=$1
DB_PASSWORD=$2
DB_PATH="$PROJECT_PATH/dev-db"

# Check arguments
if [ "$#" -lt 2 ]; then
 echo -e "${RED}Usage: $0 <db-user> <db-password>${RESET}"
 exit 1
fi

touch "$DB_PATH/docker-compose.yml"
echo "services:" >> "$DB_PATH/docker-compose.yml"

readarray -t dirs < <(find $DB_PATH -mindepth 1 -maxdepth 1 -type d -printf "%f\n")

for dir in "${dirs[@]}"; do
    TEMPLATE_PATH="$DB_PATH/$dir/docker-compose.template.yml"
    DB_DATA_PATH="$DB_PATH/$dir/data"

    mkdir -p $DB_DATA_PATH
    sed -e "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" \
        -e "s|{{PROJECT_PATH}}|$DB_DATA_PATH|g" \
        -e "s|{{DB_USER}}|$DB_USER|g" \
        -e "s|{{DB_PASSWORD}}|$DB_PASSWORD|g" \
    $TEMPLATE_PATH >> "$DB_PATH/docker-compose.yml"
done

echo -e "Docker Compose file generated at $DB_PATH/docker-compose.yml"
echo -e "Database files stored at $DB_PATH/*/data"
echo -e "To start the database(s), run 'docker compose up -d' in $DB_PATH"



