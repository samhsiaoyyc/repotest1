FROM python:3.6-slim
LABEL maintainers="block.chen@thinkpower-info.com, kevin@seasalt.ai"

# setup dev-tools
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
  build-essential \
  wget \
  openssh-client \
  graphviz-dev \
  pkg-config \
  git-core \
  openssl \
  libssl-dev \
  libffi6 \
  libffi-dev \
  libpng-dev \
  iputils-ping
RUN pip install rasa-x==0.26.3 -i https://pypi.rasa.com/simple
# Remove packages we don't need after installation
# TODO: Identify things we don't need after installation
RUN apt-get -y remove wget
# setup work dir
RUN ["mkdir", "/opt/seasalt"]
RUN ["mkdir", "/opt/seasalt/ngChat"]
RUN ["mkdir", "/tmp/tracks"]
WORKDIR /opt/seasalt/ngChat
# Copy requirements common to all bots.
COPY /bots/common_requirements.txt* ./
RUN pip install -r common_requirements.txt
# Copy and run bot-specific requirements if the requirements.txt file exists in
# the bot directory.
COPY /bots/test_bot/requirements.txt* ./
RUN [ -f requirements.txt ] && pip install -r requirements.txt
# copy ngchat common module into image
COPY ngchat_plugins/ /opt/seasalt/ngChat/ngchat_plugins/
# You can use -v argument in command "docker run" for mounting folders on container instead of copy files into the image
COPY bots/ /opt/seasalt/ngChat/bots/
COPY ngchat_cart/ /opt/seasalt/ngChat/ngchat_cart
COPY credentials.yml /opt/seasalt/ngChat/credentials.yml
# Add ngchat_plugins path into python importing scope
# So you can write something like "from common.actions.example_action import
# ActionHelloWorld" in your python code
ENV PYTHONPATH="/opt/seasalt/ngChat"
