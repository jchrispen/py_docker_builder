#*-------------------------------------------------------------------
# Stage 0: setup variables for this project

# Set base image, directories, and versions in a compact manner
ARG BASE_IMAGE_NAME=ubuntu \
    BASE_IMAGE_VERSION=23.10 \
    LOCAL_DIR=/usr/local \
    BUILD_DIR=/opt/builder \
    PYTHON_MAJOR_VERSION=3.12 \
    PYTHON_MINOR_VERSION=.1 \
    NODE_VERSION=21.6.0 \
    NPM_VERSION=10.3.0 \
    BOT_URL="https://github.com/Innovation-Web-3-0-Blockchain/Arbitrage-Bot.git"

# Construct variables based on ARGs defined above
ARG BASE_IMAGE=${BASE_IMAGE_NAME}:${BASE_IMAGE_VERSION} \
    PYTHON_VERSION=${PYTHON_MAJOR_VERSION}${PYTHON_MINOR_VERSION} \
    PYTHON_DIR=Python-${PYTHON_VERSION} \
    PYTHON_TARBALL=${PYTHON_DIR}.tar.xz \
    PYTHON_SOURCE=${BUILD_DIR}/${PYTHON_TARBALL} \
    PYTHON_BUILD_DIR=${BUILD_DIR}/${PYTHON_DIR} \
    PYTHON_PATH=${LOCAL_DIR}/${PYTHON_DIR} \
    PYTHON_URL=https://www.python.org/ftp/python/${PYTHON_VERSION}/${PYTHON_TARBALL} \
    NODE_DIR=node-v${NODE_VERSION}-linux-x64 \
    NODE_TARBALL=${NODE_DIR}.tar.xz \
    NODE_SOURCE=${BUILD_DIR}/${NODE_TARBALL} \
    NODE_PATH=${LOCAL_DIR}/${NODE_DIR} \
    NODE_URL=https://nodejs.org/dist/v${NODE_VERSION}/${NODE_TARBALL} \
    BOT_DIR=${LOCAL_DIR}/arbitrage-bot

#*-------------------------------------------------------------------
# Stage 1: Build packages you need for production
FROM ${BASE_IMAGE} as builder

# redeclare ARG variables
ARG LOCAL_DIR
ARG BUILD_DIR
ARG PYTHON_MAJOR_VERSION
ARG PYTHON_BUILD_DIR
ARG PYTHON_SOURCE
ARG PYTHON_PATH
ARG PYTHON_URL
ARG NODE_SOURCE
ARG NODE_PATH
ARG NODE_URL
ARG BOT_URL
ARG BOT_DIR

# setup variables for the project
ENV BUILDER_PACKAGES \
        git \
        nano \
        vim \
        ca-certificates \
        build-essential \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        wget \
        curl \
        llvm \
        libncurses5-dev \
        libncursesw5-dev \
        xz-utils \
        tk-dev \
        libffi-dev \
        liblzma-dev \
        python3-openssl \
        libgdbm-dev \
        libnss3-dev \
        libssl-dev \
        libreadline-dev \
        libffi-dev \
        uuid-dev

# update distro and install required packages
RUN set -x \
        && apt-get update \
        && apt-get dist-upgrade -y \
        && apt-get install -y ${BUILDER_PACKAGES}

# Create the tarball directory
RUN mkdir --parent ${BUILD_DIR}

# Set the PATH environment variable
ENV PATH=${NODE_PATH}/bin:${PYTHON_PATH}/bin:$PATH

# Check if the Python tarball exists and download if not
RUN if [ ! -f ${PYTHON_SOURCE} ]; then \
      wget --show-progress -O ${PYTHON_SOURCE} ${PYTHON_URL}; \
    fi

# Check if the Node.js tarball exists and download if not
RUN if [ ! -f ${NODE_SOURCE} ]; then \
      wget --show-progress -O ${NODE_SOURCE} ${NODE_URL}; \
    fi

# configure, make, make install Python
RUN  set -x \
      && tar -xf ${PYTHON_SOURCE} -C ${BUILD_DIR} \
      && cd ${PYTHON_BUILD_DIR} \
      && ./configure --enable-optimizations --prefix=${PYTHON_PATH} \
      && make -j $(nproc) \
      && make install \
      && ln -s ${PYTHON_PATH}/python${PYTHON_MAJOR_VERSION} ${PYTHON_PATH}/bin/python \
      && ln -s ${PYTHON_PATH}/pip${PYTHON_MAJOR_VERSION} ${PYTHON_PATH}/bin/pip

# install Node.js
RUN  set -x \
      && tar -xf ${NODE_SOURCE} -C ${LOCAL_DIR} \
      && cd ${NODE_PATH} \
      && npm install -g npm@${NPM_VERSION}

# Clone or update the git repo
RUN if [ -d "${BOT_DIR}" ]; then \
      echo "Pulling repository ..."; \
      cd ${BOT_DIR}; \
      git pull --all --prune --tags; \
    else \
      echo "Cloning repository ..."; \
      git clone ${BOT_URL} ${BOT_DIR}; \
    fi

RUN if [ -d "${BOT_DIR}" ]; then \
      echo "Installing npm packages ..."; \
      cd ${BOT_DIR}; \
      npm install; \
  # TODO: find a way to target the smart contracts \
      npm audit fix --force; \
    fi


#*-------------------------------------------------------------------
# Stage 2: Production image
FROM ${BASE_IMAGE}

# redeclare ARG variables
ARG PYTHON_PATH
ARG NODE_PATH
ARG LOCAL_DIR

# Set the default command to execute
# when creating a new container
CMD ["bash"]

# Set the PATH environment variable
ENV PATH=${NODE_PATH}/bin:${PYTHON_PATH}/bin:$PATH

# setup variables for the project
ENV PROD_PACKAGES \
        speedtest-cli \
        git \
        nano \
        vim

# Update and upgrade all packages, remove unused dependencies
# Install packages and environment
RUN set -x \
        && apt-get update \
        && apt-get dist-upgrade -y \
        && apt-get install -y ${PROD_PACKAGES} \
    # clean up packages
        && apt-get autoremove -y \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# copy the packages built in previous stage(s)
COPY --from=builder ${LOCAL_DIR} ${LOCAL_DIR}


#*-------------------------------------------------------------------
# Stage End
