#!/bin/bash

# Exit on error
set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

PROJECT_INIT_PATH="$HOME/.devtools/project-init"

ADD_SCHOOL={{ADD_SCHOOL}}

completed() {
  echo -e "${GREEN}✓${RESET} Completed"
}

script_help() {
  echo "Usage: project-init <project-type> <repository-name> [--db database-types] [commit-message]"
    echo "  Mandatory arguments:"
    echo "    -p                 Personal projects"
    if [ "$ADD_SCHOOL" == "y" ]; then
      echo "    -s                 School projects"
    fi
    echo "    <repository-name>  The name of the repository"
    echo ""
    echo "  Optional arguments:"
    echo "    --db              Comma-separated list of database types to setup"
    echo "                      Options: postgres, mongodb, chroma"
    echo "                      Example: --db postgres,mongodb"
    echo "    [commit-message]   The commit message for the initial commit"
    echo "                      Default: 'feat: <repository-name> initial commit'"
    exit 1
}

# Check arguments
if [ "$#" -lt 2 ]; then
  if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    script_help
  fi
  script_help
fi

REPO_TYPE=$1
REPO_NAME=$2
DATABASES=""
COMMIT_MESSAGE="feat: $REPO_NAME initial commit"

### PARSE ARGUMENTS ###

# Parse remaining arguments
shift 2  # Remove first two arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --db)
      if [ -n "$2" ]; then
        DATABASES=$2
        shift 2
      else
        echo -e "${RED}Error: --db requires a comma-separated list of database types${RESET}"
        exit 1
      fi
      ;;
    *)
      COMMIT_MESSAGE="$1"
      shift
      ;;
  esac
done

# Check project flag to determine base path

case "$REPO_TYPE" in
  -p)
    BASE_PATH=$PERSONAL_PATH
    ;;
  -s)
    if [ "$ADD_SCHOOL" != "y" ]; then
      echo -e "${RED}School projects are not enabled. Please use -p for personal projects.${RESET}"
      exit 1
    fi
    BASE_PATH=$SCHOOL_PATH
    ;;
  *)
    echo -ne "${RED}Invalid repository type. Use -p for personal projects"
    if [ "$ADD_SCHOOL" == "y" ]; then
      echo -n " or -s for school projects"
    fi
    echo -n ".${RESET}"
    exit 1
    ;;
esac

### DIRECTORY INIT ###

LOCAL_PATH="$BASE_PATH/$REPO_NAME"

# Ensure the local path exists
if [ ! -d "$LOCAL_PATH" ]; then
  echo -e "${YELLOW}The specified folder '$REPO_NAME' does not exist in $BASE_PATH. Creating it...${RESET}"
  mkdir -p "$LOCAL_PATH"
fi
completed

cd "$LOCAL_PATH"

# Create a README file
echo -e "${CYAN}Creating README file...${RESET}"
echo "# Welcome to $REPO_NAME" > README.md
cat "$PROJECT_INIT_PATH/setup-db.md" >> README.md
completed

# Create a .env file
echo -e "${CYAN}Creating .env file...${RESET}"
touch .env
completed


# Generate build and deployement scripts
echo -e "${CYAN}Generating build and deployment scripts...${RESET}"
mkdir -p "$LOCAL_PATH/build"
cp "$PROJECT_INIT_PATH/build.sh" "$LOCAL_PATH/build/build.sh"
cp "$PROJECT_INIT_PATH/deploy.sh" "$LOCAL_PATH/build/deploy.sh"

sed -i "s|{{PROJECT_NAME}}|$REPO_NAME|g" "$LOCAL_PATH/build/build.sh"
sed -i "s|{{PROJECT_NAME}}|$REPO_NAME|g" "$LOCAL_PATH/build/deploy.sh"

chmod +x "$LOCAL_PATH/build/build.sh"
chmod +x "$LOCAL_PATH/build/deploy.sh"

# Create Dockerfile
echo -e "${CYAN}Creating Dockerfile...${RESET}"
touch "$LOCAL_PATH/build/Dockerfile"
touch "$LOCAL_PATH/docker-compose.yml"

completed

# Add .gitignore file with at least .env in it
echo -e "${CYAN}Adding .gitignore file...${RESET}"
echo ".env" >> .gitignore
echo "dev-db/*/data" >> .gitignore
echo "dev-db/docker-compose.yml" >> .gitignore
completed

### DATABASE INIT ###

if [ -n "$DATABASES" ]; then

  mkdir -p "$LOCAL_PATH/dev-db"

  # Function to setup a specific database
  setup_database() {
    local db_type=$1
    case $db_type in
     postgres)
        echo -e "${CYAN}Setting up PostgreSQL development database...${RESET}"
        mkdir -p "$LOCAL_PATH/dev-db/postgres"
        cp "$PROJECT_INIT_PATH/postgres.template.yml" "$LOCAL_PATH/dev-db/postgres/docker-compose.template.yml"
        completed
        ;;
      mongodb)
        echo -e "${CYAN}Setting up MongoDB development database...${RESET}"
        mkdir -p "$LOCAL_PATH/dev-db/mongodb"
        cp "$PROJECT_INIT_PATH/mongo.template.yml" "$LOCAL_PATH/dev-db/mongodb/docker-compose.template.yml"
        completed
        ;;
      chroma)
        echo -e "${CYAN}Setting up Chroma development database...${RESET}"
        mkdir -p "$LOCAL_PATH/dev-db/chroma"
        cp "$PROJECT_INIT_PATH/chroma.template.yml" "$LOCAL_PATH/dev-db/chroma/docker-compose.template.yml"
        completed
        ;;
      *)
        echo -e "${RED}Warning: Unknown database type '$db_type' - skipping${RESET}"
        ;;
    esac
  }

  # Setup each requested database
  IFS=',' read -ra DB_ARRAY <<< "$DATABASES"
  for db in "${DB_ARRAY[@]}"; do
   setup_database $(echo $db | tr -d ' ')  # Remove any whitespace
  done

  cp "$PROJECT_INIT_PATH/setup-db.sh" "$LOCAL_PATH/dev-db/setup.sh"
  chmod +x "$LOCAL_PATH/dev-db/setup.sh"
fi

### GIT INIT ###

# Create a new GitHub repository
echo -e "${CYAN}Creating repository '$REPO_NAME' on GitHub as private...${RESET}"
gh repo create "$REPO_NAME" --private

# Initialize a local Git repository
echo -e "${CYAN}Initializing local repository in $LOCAL_PATH...${RESET}"
git init

# Link the remote repository
REMOTE_URL="git@github.com:$GIT_USERNAME/$REPO_NAME.git"
echo -e "${CYAN}Setting up remote repository at $REMOTE_URL...${RESET}"
git remote add origin "$REMOTE_URL"

# Stage and commit changes
echo -e "${CYAN}Committing changes...${RESET}"
git add .
git commit -m "$COMMIT_MESSAGE"

# Push to GitHub
echo -e "${CYAN}Pushing to GitHub...${RESET}"
git branch -M main
git push -u origin main

echo -e "${GREEN}Repository '$REPO_NAME' has been created at $LOCAL_PATH and pushed to GitHub.${RESET}"
