#*-------------------------------------------------------------------
# This script creates a docker container and initalizes the
# arbitrage-bot so that it can be run in a containerd space.
#
# The docker image builds on the python:<version>-slim image and
# installs Node.js and the git repo for the bot project.
#*-------------------------------------------------------------------

#*-------------------------------------------------------------------
# Stage 0: setup variables for this project

# Set base image, directories, and versions in a compact manner
ARG PYTHON_MAJOR_VERSION=3.12 \
    PYTHON_MINOR_VERSION=.1 \
    NODE_VERSION=21.6.0 \
    NPM_VERSION=10.3.0 \
    BOT_URL="https://github.com/Innovation-Web-3-0-Blockchain/Arbitrage-Bot.git" \
    BASE_IMAGE_NAME=python \
    LOCAL_DIR=/usr/local \
    BUILD_DIR=/opt/builder \
    BASE_PACKAGES=" \
        speedtest-cli \
        git \
        nano \
        vim \
        wget \
        curl \
        xz-utils"

# Construct variables based on ARGs defined above
ARG BASE_IMAGE_VERSION=${PYTHON_MAJOR_VERSION}-slim \
    BASE_IMAGE=${BASE_IMAGE_NAME}:${BASE_IMAGE_VERSION} \
    PYTHON_VERSION=${PYTHON_MAJOR_VERSION}${PYTHON_MINOR_VERSION} \
    NODE_DIR=node-v${NODE_VERSION}-linux-x64 \
    NODE_TARBALL=${NODE_DIR}.tar.xz \
    NODE_SOURCE=${BUILD_DIR}/${NODE_TARBALL} \
    NODE_PATH=${LOCAL_DIR}/${NODE_DIR} \
    NODE_URL=https://nodejs.org/dist/v${NODE_VERSION}/${NODE_TARBALL} \
    BOT_DIR=${LOCAL_DIR}/arbitrage-bot


#*-------------------------------------------------------------------
# Stage 1: Build the base image for later stages to use
# Keep this image clean for use in the final_production image
FROM ${BASE_IMAGE} as base_image

# setup variables for the project
ARG BASE_PACKAGES

# update distro and install required packages
RUN set -x \
        && apt-get update \
        && apt-get dist-upgrade -y \
        && apt-get install -y ${BASE_PACKAGES} \
    # clean up packages
        && apt-get autoremove -y \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*


#*-------------------------------------------------------------------
# Stage 2: Install Node.js
FROM base_image as node_builder

# redeclare ARG variables
ARG BUILD_DIR
ARG LOCAL_DIR
ARG NODE_SOURCE
ARG NODE_URL

# Check if the Node.js tarball exists and download if not
RUN if [ ! -f ${NODE_SOURCE} ]; then \
      # Create the build directory
      mkdir --parent ${BUILD_DIR}; \
      wget --show-progress -O ${NODE_SOURCE} ${NODE_URL}; \
    fi

# install Node.js
RUN if [ ! -f ${NODE_SOURCE} ]; then exit 1; fi \
    && tar -xf ${NODE_SOURCE} -C ${LOCAL_DIR}


#*-------------------------------------------------------------------
# Stage 3: Install Bot
FROM base_image as bot_builder

# redeclare ARG variables
ARG BOT_URL
ARG BOT_DIR

# Clone or update the git repo
RUN if [ -d "${BOT_DIR}" ]; then \
      echo "Pulling repository ..."; \
      cd ${BOT_DIR}; \
      git pull --all --prune --tags; \
    else \
      echo "Cloning repository ..."; \
      git clone ${BOT_URL} ${BOT_DIR}; \
    fi


#*-------------------------------------------------------------------
# Stage 4: Bring it together and update anything that needs it
FROM base_image as pre_production

# redeclare ARG variables
ARG LOCAL_DIR
ARG BOT_DIR
ARG NODE_PATH
ARG NPM_VERSION

# copy the packages built in previous stage(s)
COPY --from=node_builder ${LOCAL_DIR} ${LOCAL_DIR}
COPY --from=bot_builder ${LOCAL_DIR} ${LOCAL_DIR}

# Set the PATH environment variable
ENV PATH=${NODE_PATH}/bin:$PATH

# update Node.js
RUN  set -x \
        && cd ${NODE_PATH} \
        && npm install -g npm@${NPM_VERSION} \
    # Install npm packages
        && echo "Installing npm packages ..." \
        && cd ${BOT_DIR} \
        && npm install \
      # TODO: find a way to target smart contracts \
        && npm audit fix --force


#*-------------------------------------------------------------------
# Stage 5: Final image
# keep as flat as possible to limit layers
FROM base_image as final_production

# redeclare ARG variables
ARG NODE_PATH
ARG LOCAL_DIR

# Set the default command to execute
# when creating a new container
CMD ["bash"]

# Set the PATH environment variable
ENV PATH=${NODE_PATH}/bin:$PATH

# copy the packages built in previous stage(s)
COPY --from=pre_production ${LOCAL_DIR} ${LOCAL_DIR}


#*-------------------------------------------------------------------
# End Stage(s)
