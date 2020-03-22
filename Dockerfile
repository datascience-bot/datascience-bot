# Build Image for Remote Container
# ----------------------------------------------------------------------------
# How long will this take?
#   First build will take 5-10 minutes. Go make a cup of coffee.
# ----------------------------------------------------------------------------
# Who wrote this image?
#   Mostly sourced from tradingai/bazel so we can update dependencies ourselves
#   as we choose
#   https://registry.hub.docker.com/r/tradingai/bazel/dockerfile
# ----------------------------------------------------------------------------
# Why use remote containers?
#   Read https://medium.com/windmill-engineering/bazel-is-the-worst-build-system-except-for-all-the-others-b369396a9e26
#   tl;dr -- build systems suck when developers have to sync their dev
#   environments. Remote containers help solve that problem by standardizing
#   the dev environment.
# ----------------------------------------------------------------------------
# What is remote development?
#   vscode makes it easy https://code.visualstudio.com/docs/remote/remote-overview
# ----------------------------------------------------------------------------
# TODO: move some of this docstring to a CONTRIBUTE.md in the root dir

FROM ubuntu:18.04

# TODO: define jdk version here
# TODO: get versions from shared VERSION file or similar
ENV BAZEL_VERSION=2.2.0 \
    GOLANG_VERSION=1.13.8 \
    PYTHON_VERSION=3.7.6 \
    PROTOBUF_VERSION=3.6.1 \
    NODEJS_VERSION=12

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    software-properties-common \
    curl \
    wget \
    git \
    gnupg \
    libopenblas-dev \
    liblapack-dev \
    libssl-dev \
    libmetis-dev \
    pkg-config \
    zlib1g-dev \
    openssh-client \
    openjdk-11-jdk \
    g++ unzip zip \
    openjdk-11-jre-headless

# Install nodejs yarn
RUN (curl -sL https://deb.nodesource.com/setup_${NODEJS_VERSION}.x | bash -) && \
    apt-get install -y nodejs && \
    (curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -) && \
    (echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list) && \
    apt-get update && apt-get install -y yarn && \
    apt-get install -y gcc-6 g++-6 && \
    rm /usr/bin/gcc /usr/bin/g++ && \
    ln -s /usr/bin/gcc-6 /usr/bin/gcc && \
    ln -s /usr/bin/g++-6 /usr/bin/g++

# Install Python
WORKDIR /tmp/
RUN wget -P /tmp https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz && \
    tar -zxvf Python-$PYTHON_VERSION.tgz

WORKDIR /tmp/Python-$PYTHON_VERSION
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

RUN apt-get install -y --no-install-recommends \
    libbz2-dev \
    libncurses5-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    liblzma-dev \
    libsqlite3-dev \
    libssl-dev \
    openssl \
    tk-dev \
    uuid-dev \
    libreadline-dev \
    libffi-dev

RUN ./configure --prefix=/usr/local/python3

RUN make && \
    make install && \
    update-alternatives --install /usr/bin/python python /usr/local/python3/bin/python3 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/local/python3/bin/pip3 1 && \
    update-alternatives --config python && \
    update-alternatives --config pip && \
    pip install --upgrade pip && \
    pip install pre-commit black && \
    touch /root/WORKSPACE

# Install Golang
RUN curl -L https://dl.google.com/go/go$GOLANG_VERSION.linux-amd64.tar.gz | tar zx -C /usr/local
ENV PATH /usr/local/go/bin:$PATH

RUN mkdir -p /go/src /go/bin && chmod -R 777 /go
ENV GOROOT=/usr/local/go \
    GOPATH=/go \
    PATH=/go/bin:$PATH

# Install go packages
RUN go env -w GO111MODULE=on && \
    go env -w GOPROXY=https://goproxy.io,direct

# replace with COPY go.mod /go.mod ??? I'm not a go programmer.
RUN go mod init datascience_bot/m && \
    go mod download

# Install proto buffer
# refer to https://github.com/golang/protobuf
RUN wget -P /tmp https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOBUF_VERSION}/protoc-${PROTOBUF_VERSION}-linux-x86_64.zip && \
    unzip /tmp/protoc-${PROTOBUF_VERSION}-linux-x86_64.zip -d protoc3 && \
    rm /tmp/protoc-${PROTOBUF_VERSION}-linux-x86_64.zip && \
    mv protoc3/bin/* /usr/local/bin/ && \
    mv protoc3/include/* /usr/local/include/

# Install GoLang proto gen
RUN go get -u -v github.com/golang/protobuf/protoc-gen-go

# Manually clone golang.org/x/XXX packages from their github mirrors.
WORKDIR /go/src/golang.org/x/
RUN git clone --progress https://github.com/golang/debug.git && \
    git clone --progress https://github.com/golang/glog.git && \
    git clone --progress https://github.com/golang/time.git && \
    git clone --progress https://github.com/golang/sync.git && \
    git clone --progress https://github.com/golang/crypto && \
    git clone --progress https://github.com/golang/tools && \
    git clone --progress https://github.com/golang/sys

# Install packr2
RUN go get -u github.com/gobuffalo/packr/v2/packr2

# Install bazel
RUN (wget -P /tmp https://github.com/bazelbuild/bazel/releases/download/$BAZEL_VERSION/bazel-$BAZEL_VERSION-installer-linux-x86_64.sh) && \
    (chmod +x /tmp/bazel-$BAZEL_VERSION-installer-linux-x86_64.sh) && \
    bash /tmp/bazel-$BAZEL_VERSION-installer-linux-x86_64.sh && \
    echo "export PATH=$PATH:/usr/lib/go/bin" >> /root/.bashrc && \
    go get github.com/bazelbuild/buildtools/buildifier

# clean
RUN rm -rf /tmp/* && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /root/.cache/pip

WORKDIR /root

RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/python3/bin/python3 1 && \
    update-alternatives --install /usr/bin/pip3 pip3 /usr/local/python3/bin/pip3 1 && \
    update-alternatives --config python3 && \
    update-alternatives --config pip3

# dirs for bazel build
RUN mkdir -p /root/cache/bazel && \
    mkdir -p /root/output

# https://github.com/pypa/pip/issues/4924
RUN mv /usr/bin/lsb_release /usr/bin/lsb_release.bak

CMD ["/bin/bash"]
