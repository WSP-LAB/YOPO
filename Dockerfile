FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir yopo-artifact

RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    git \
    vim \
    tmux \
    curl \
    nodejs \
    npm \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libxt6 \
    libx11-xcb1 \
    libxcomposite1  \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    liblzma-dev \
    libxdamage1 \
    libxrandr2 \
    libxcb1 \
    libxcursor1 \
    libxinerama1 \
    libasound2 \
    libpango1.0-0 \
    libxss1 \
    libnss3 \
    libegl1 \
    zip \
    xvfb \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update

# Install Python 3.9 and related packages
RUN apt-get install -y \
    python3.9 \
    python3.9-distutils \
    python3.9-dev \
    python3.9-venv \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh -O /tmp/anaconda.sh \
    && bash /tmp/anaconda.sh -b -p /opt/anaconda \
    && rm /tmp/anaconda.sh

ENV PATH="/opt/anaconda/bin:$PATH"
RUN /opt/anaconda/bin/conda init bash

COPY . /yopo-artifact

WORKDIR /yopo-artifact

RUN conda create -n adgraph python=3.8.15 -y \
    && conda run -n adgraph pip install --no-cache-dir -r ./requirements_adgraph.txt

RUN conda create -n python2 python=2.7.18 -y \
    && conda run -n python2 pip install --no-cache-dir -r ./requirements_python2.txt

RUN conda create -n adflush python=3.8.19 -y \
    && conda run -n adflush pip install --no-cache-dir -r ./requirements_adflush.txt

# Install mitmproxy and venv environment
RUN cd /yopo-artifact/mitmproxy && ./dev.sh

RUN chmod 755 /opt/anaconda/etc/profile.d/conda.sh

# Install conda environment for OpenWPM
RUN cd /yopo-artifact/OpenWPM && ./install.sh

# Install nvm & upgrade nodejs
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash && \
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && \
    nvm install 19.8.1 && \
    nvm use 19.8.1 && \
    nvm alias default 19.8.1

# Install brave browser
RUN curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] https://brave-browser-apt-release.s3.brave.com/ stable main" | tee /etc/apt/sources.list.d/brave-browser.list
RUN apt-get update && apt-get install -y brave-browser=1.68.134 --allow-downgrades && rm -rf /var/lib/apt/lists/*

CMD ["tail", "-f", "/dev/null"]
