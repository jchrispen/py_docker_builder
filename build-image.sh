#!/usr/bin/env bash

# List of required dependencies
dependencies=("docker" "service" "date" "git") # Update this list based on apps required
# List of required files
required_files=("Dockerfile") # Update this list based on your needs

# exit if any command exits with a non-zero
set -e

# Function to handle errors
error_exit()
{
    echo "Error: $1" 1>&2
    exit 1
}

# Function to check for the presence of a command
check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        error_exit "Error: Required command '$1' is not installed."
    fi
}

# Function to check for the presence of a file
check_file_presence() {
    if [ ! -f "$1" ]; then
        echo "Error: Required file '$1' is not present in the current directory." 1>&2
        exit 1
    fi
}

# Check for required dependencies
for dep in "${dependencies[@]}"; do
    check_dependency "$dep"
done

# Check for required files
for file in "${required_files[@]}"; do
    check_file_presence "$file"
done

clear # the screen

# check if Docker is running
if ! service docker status &> /dev/null; then
    echo "Docker is not running, attempting to start Docker..."
    sudo service docker start || error_exit "Failed to start Docker."
    # Wait for Docker to start
    sleep 1
fi

# list containers and images before starting
docker ps -a  || error_exit "Failed to list Docker containers."
docker images || error_exit "Failed to list Docker images."
echo

# create timestamp for this run
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Get the latest Git commit hash
GIT_COMMIT_HASH=$(git rev-parse --short HEAD)

# Check if the git command was successful
if [ $? -ne 0 ]; then
    echo "Warning: Failed to get Git commit hash. Proceeding without it."
    IMAGE_TAG="arbitrage-bot:${TIMESTAMP}"
else
    IMAGE_TAG="arbitrage-bot:${TIMESTAMP}-${GIT_COMMIT_HASH}"
fi

# build docker image
docker buildx build -t "${IMAGE_TAG}" . || error_exit "Docker build failed."
# create container
docker create -it --name bot-"${TIMESTAMP}" "${IMAGE_TAG}" || error_exit "Failed to create Docker container."

# list containers and images afterwards
docker ps -a  || error_exit "Failed to list Docker containers."
docker images || error_exit "Failed to list Docker images."
echo
echo "Script completed successfully."

exit 0
