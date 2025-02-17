FROM nvcr.io/nvidia/pytorch:21.07-py3 AS application

ARG PARTNER_NAME
ARG SERVICE_NAME
ARG VERSION
ARG MONAI_APP_MODULE
ARG MODEL_PATH
ARG EXTRA_PYTHON_PACKAGES

ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# python3-gdcm or python-gdcm is required for decompression
RUN apt-get -y update && \
    apt-get -y install --no-install-recommends python3-distutils python3-gdcm && \
    # apt-get -y install python3.7 && \
    apt-get autoclean && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV DEBUG=YES
ENV KEEP_FILES=YES

# make sure all messages reach the console
ENV PYTHONUNBUFFERED=1

# copy MONAI app files
COPY . /app/.
WORKDIR /app

# copy model file to model folder
RUN wget -q https://github.com/Project-MONAI/model-zoo/releases/download/hosting_storage_v1/lung_nodule_ct_detection_v0.2.0.zip && \
    unzip lung_nodule_ct_detection_v0.2.0.zip -d /tmp/ && \
    cp /tmp/lung_nodule_ct_detection/models/model.ts model/. && \
    rm -rf /tmp/lung_nodule_ct_detection && \
    rm lung_nodule_ct_detection_v0.2.0.zip

# non-root aiserviceuser in group aiserviceuser with UserID and GroupID as 20225
RUN groupadd -g 20225 -r aiserviceuser && useradd -u 20225 -r -g aiserviceuser aiserviceuser && chown -R aiserviceuser:aiserviceuser /app && \
    chown -R aiserviceuser:aiserviceuser /var
USER aiserviceuser:aiserviceuser

ENV VIRTUAL_ENV=.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m pip install --upgrade pip && \
    python -m pip install --upgrade --no-cache-dir ${EXTRA_PYTHON_PACKAGES} -r requirements.txt && \
    python -m pip install --upgrade --no-cache-dir lib/ai_service-*-py3-none-any.whl && \
    pip install --upgrade numpy && \
    rm -rf lib && \
    rm requirements.txt

ENV AI_PARTNER_NAME ${PARTNER_NAME}
ENV AI_SVC_NAME ${SERVICE_NAME}
ENV AI_SVC_VERSION ${VERSION}
ENV AI_MODEL_PATH ${MODEL_PATH}
ENV MONAI_APP_CLASSPATH ${MONAI_APP_MODULE}

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
CMD ["python", "app_wrapper.py"]
