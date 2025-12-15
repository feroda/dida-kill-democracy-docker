FROM ubuntu:16.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        python2.7 \
        python-pip \
        zenity \
        x11-apps \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Symlink comodo
# RUN ln -s /usr/bin/python2.7 /usr/bin/python

CMD ["bash"]
