FROM python:3.9.16-slim

ENV DEBIAN_FRONTEND=noninteractive 

ARG USER_NAME
ARG USER_ID
ARG USER_GID

# # ==============================================================================
# #                          UBUNTU USERS CREATION
# # ==============================================================================

RUN /usr/sbin/groupadd --non-unique --gid ${USER_GID} ${USER_NAME} && \
    /usr/sbin/useradd -ms /bin/bash --gid ${USER_NAME} --uid ${USER_ID} ${USER_NAME}

RUN apt-get clean
RUN apt-get update

WORKDIR /indexado-streamlit

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . /indexado-streamlit

RUN python -m spacy download en_core_web_trf

EXPOSE 8502
CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0", "--server.port", "8502", "--server.fileWatcherType", "none"]