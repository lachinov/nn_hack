FROM fenixfly/vinodock

USER root
WORKDIR /

RUN pip3 install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html onnxruntime-gpu

COPY . /app

ENTRYPOINT [ "bash" , "-l", "-c" ]