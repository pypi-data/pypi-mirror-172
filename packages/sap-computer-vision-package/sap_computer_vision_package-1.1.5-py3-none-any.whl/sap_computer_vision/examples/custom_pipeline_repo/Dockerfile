FROM python
RUN apt update -y && \
    apt install -y libglib2.0-0 libjpeg62-turbo-dev libtiff-dev libpng-dev libsm6 libxrender1 libxext6 libgl1-mesa-glx build-essential wget git zip && \
    apt install -y imagemagick
WORKDIR /sap_cv
ENV HOME=/sap_cv
RUN python -m pip install --upgrade pip
RUN python -m pip install numpy pillow

COPY . sap_cv/synthesize_image
USER root

WORKDIR /sap_cv/synthesize_image
ENV HOME=/sap_cv/synthesize_image

RUN mkdir -p /tmp/dataout
RUN chgrp -R nogroup /tmp && \
    chmod -R 777 /tmp
RUN chgrp -R nogroup /sap_cv && \
    chmod -R 777 /sap_cv
