FROM mcr.microsoft.com/azureml/base:intelmpi2018.3-ubuntu16.04
#FROM dvaew1afahubacr02.azurecr.io/project/mcma/mcma_big_data_et_innovation/rami_attachments_text_extract:1.0.4

WORKDIR home

RUN apt-get update
RUN apt-get -y install curl

RUN mkdir ml-cli
RUN cd ml-cli
ENV CURRENT_VERSION=v0.46.0

# Download ml-cli-web
RUN curl -L https://github.com/AxaGuilDEv/ml-cli/releases/download/${CURRENT_VERSION}/linux-x64-ml-cli.zip --output ml-cli.zip
RUN unzip ml-cli.zip -d ./ml-cli
RUN chmod +x /home/ml-cli/Ml.Cli