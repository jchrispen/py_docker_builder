#*-------------------------------------------------------------------
# Stage 0: setup variables for this project

# Set common variables
ARG LOCAL_DIR=/usr/local
ARG TARBALLS_DIR=/opt/builder/tarball

# Set python variables
ARG PYTHON_MAJOR_VERSION=3.12
ARG PYTHON_MINOR_VERSION=.1
ARG PYTHON_VERSION=${PYTHON_MAJOR_VERSION}${PYTHON_MINOR_VERSION}
ARG PYTHON_TARBALL=Python-${PYTHON_VERSION}.tar.xz
ARG PYTHON_SOURCE=${TARBALLS_DIR}/${PYTHON_TARBALL}
ARG PYTHON_PATH=${LOCAL_DIR}/python-v${PYTHON_VERSION}/bin
ARG PYTHON_URL=https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz

# Set node.js variables
ARG NODE_VERSION=21.6.0
ARG NODE_TARBALL=node-v${NODE_VERSION}-linux-x64.tar.xz
ARG NODE_SOURCE=${TARBALLS_DIR}/${NODE_TARBALL}
ARG NODE_PATH=${LOCAL_DIR}/node-v${NODE_VERSION}-linux-x64/bin
ARG NODE_URL=https://nodejs.org/dist/v${NODE_VERSION}/${NODE_TARBALL}

# Arbitrage bot variables
ARG BOT_URL="https://github.com/Innovation-Web-3-0-Blockchain/Arbitrage-Bot.git"
ARG BOT_DIR=${LOCAL_DIR}/arbitrage-bot


#*-------------------------------------------------------------------
# Stage 1: Build packages you need for production
FROM ubuntu:23.10 as builder

# redeclare ARG variables
ARG LOCAL_DIR
ARG TARBALLS_DIR
ARG PYTHON_MAJOR_VERSION
ARG PYTHON_MINOR_VERSION
ARG PYTHON_VERSION
ARG PYTHON_TARBALL
ARG PYTHON_SOURCE
ARG PYTHON_PATH
ARG PYTHON_URL
ARG NODE_VERSION
ARG NODE_TARBALL
ARG NODE_SOURCE
ARG NODE_PATH
ARG NODE_URL
ARG BOT_URL
ARG BOT_DIR

# setup variables for the project
ENV BUILDER_PACKAGES \
        software-properties-common \
        wget \
        git \
        nano \
        vim \
        build-essential \
        libssl-dev \
        zlib1g-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libreadline-dev \
        libsqlite3-dev \
        libgdbm-dev \
        libdb5.3-dev \
        libbz2-dev \
        libexpat1-dev \
        liblzma-dev \
        tk-dev \
        libffi-dev

# update distro and install required packages
RUN set -x \
      && apt-get update \
      && apt-get install -y ${BUILDER_PACKAGES}

# Create the tarball directory
RUN mkdir --parent ${TARBALLS_DIR}

# Check if the Python tarball exists and download it if not
RUN if [ ! -f ${PYTHON_SOURCE} ]; then \
      wget --show-progress -O ${PYTHON_SOURCE} ${PYTHON_URL}; \
    fi

# Check if the Node.js tarball exists and download it if not
RUN if [ ! -f ${NODE_SOURCE} ]; then \
      wget --show-progress -O ${NODE_SOURCE} ${NODE_URL}; \
    fi

# build and install Python
RUN  set -x \
      && cd ${TARBALLS_DIR} \
      && tar -xf ${PYTHON_TARBALL} \
      && cd Python-${PYTHON_VERSION} \
      && ./configure --enable-optimizations --prefix=${LOCAL_DIR}/python-v${PYTHON_VERSION} \
      && make -j $(nproc) \
      && make install

# install Node.js
RUN  set -x \
      && cd ${TARBALLS_DIR} \
      && tar -xf ${NODE_TARBALL} -C ${LOCAL_DIR}

# Set the PATH environment variable
ENV PATH=${NODE_PATH}:${PYTHON_PATH}:$PATH

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
    fi


#*-------------------------------------------------------------------
# Stage 2: Production image
FROM ubuntu:23.10

# redeclare ARG variables
ARG PYTHON_MAJOR_VERSION
ARG PYTHON_MINOR_VERSION
ARG PYTHON_VERSION
ARG PYTHON_PATH
ARG NODE_VERSION
ARG NODE_PATH
ARG LOCAL_DIR

# setup variables for the project
ENV PROD_PACKAGES \
        speedtest-cli \
        git \
        nano \
        vim

# copy the packages built in previous stage(s)
COPY --from=builder ${LOCAL_DIR} ${LOCAL_DIR}

# Set the PATH environment variable
ENV PATH=${NODE_PATH}:${PYTHON_PATH}:$PATH

# Configure packages and environment
RUN set -x \
        && apt-get update \
        && apt-get dist-upgrade -y \
        && apt-get install -y ${PROD_PACKAGES} \
    # clean up packages
        && apt-get autoremove -y \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
    # configure python
        && ln -s ${LOCAL_DIR}/python-v${PYTHON_VERSION}/bin/python${PYTHON_MAJOR_VERSION} /usr/bin/python \
        && ln -s ${LOCAL_DIR}/python-v${PYTHON_VERSION}/bin/pip${PYTHON_MAJOR_VERSION} /usr/bin/pip

# Set the default command to execute
# when creating a new container
CMD ["bash"]

#*-------------------------------------------------------------------
# Stage End
