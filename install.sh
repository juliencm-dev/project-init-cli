#!/bin/bash

# Exit on error
set -e

# Color codes
RED='\033[0;31m'
PURPLE='\033[0;35m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RESET='\033[0m'

completed() {
  echo -e "${GREEN}✓${RESET} Completed"
}

echo -e "${PURPLE}                         __               __             __        __  __ "   
echo -e " _____________  ____    |__| ____   _____/  |_          |__| ____ |__|/  |_ " 
echo -e " \____ \_  __ \/  _ \   |  |/ __ \_/ ___\   __\  ______ |  |/    \|  \   __\ "
echo -e " |  |_> >  | \(  <_> )  |  \  ___/\  \___|  |   /_____/ |  |   |  \  ||  | "  
echo -e " |   __/|__|   \____/\__|  |\___  >\___  >__|           |__|___|  /__||__| "  
echo -e " |__|               \______|    \/     \/                       \/ ${RESET}" 
echo -e " " 
echo -e "${YELLOW}Welcome to the project-init cli installation script!${RESET}"
echo -e "Follow the instructions below to install to setup the different environment variables."
echo -e "Before using project-init, make sure you have Git, Github CLI, Docker and Docker Compose installed."
echo -e "Press enter to continue or Ctrl+C to exit."
read -r

echo -e "${YELLOW}Setting up project-init directory${RESET}"

LOCAL_PATH=$(pwd)
INSTALL_PATH="$HOME/.devtools/project-init"

mkdir -p $INSTALL_PATH
cp -r $LOCAL_PATH/src/* $INSTALL_PATH/

echo '
# project-init environment variables
' >> "$HOME/.bashrc"

completed

### SETUP ENVIRONMENT VARIABLES ###
## GITHUB USERNAME ##

echo -e "${YELLOW}Setting up environment variables${RESET}"
read -p "Github username (required): " -r USERNAME

while [ -z "$USERNAME" ]; do
  echo -e "${RED}Github username is required.${RESET}"
  read -p "Github username (required): " -r USERNAME
done

echo "export GIT_USERNAME=$USERNAME" >> "$HOME/.bashrc"
completed

## PERSONAL PROJECTS PATH ##

read -p "Personal projects path (required): " -r PERSONAL_PATH

while [ -z "$PERSONAL_PATH" ]; do
  echo -e "${RED}Personal projects path is required.${RESET}"
  read -p "Personal projects path (required): " -r PERSONAL_PATH
done

echo "export PERSONAL_PATH=$PERSONAL_PATH" >> "$HOME/.bashrc"
completed

## ADD SCHOOL PROJECTS DIRECTORY ##

read -p "Do you wish to add a school projects directory? (y/n) " -r ADD_SCHOOL

sed "s|{{ADD_SCHOOL}}|$ADD_SCHOOL|g" "$INSTALL_PATH/scripts/launch.sh" > "$INSTALL_PATH/scripts/launch.sh.tmp"
mv "$INSTALL_PATH/scripts/launch.sh.tmp" "$INSTALL_PATH/scripts/launch.sh"

if [ "$ADD_SCHOOL" == "y" ]; then
  read -p "School projects path$ (required): " -r SCHOOL_PATH

  while [ -z "$SCHOOL_PATH" ]; do
    echo -e "${RED}School projects path is required.${RESET}"
    read -p "School projects path (required): " -r SCHOOL_PATH
  done

  echo "export SCHOOL_PATH=$SCHOOL_PATH" >> "$HOME/.bashrc"
  completed
fi

## CREATE PROJECT-INIT ALIAS ##

echo -e "${YELLOW}Creating project-init alias${RESET}"
echo '
project-init() {
  "$HOME/.devtools/project-init/scripts/launch.sh" "$@"
}
' >> "$HOME/.bashrc"
completed

chmod +x "$INSTALL_PATH/scripts/launch.sh"

echo -e "To get started, run 'project-init -h' to see the available commands."
echo -e "Happy coding! 🚀"

source ~/.bashrc
