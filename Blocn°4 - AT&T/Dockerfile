FROM tensorflow/tensorflow:latest-gpu

WORKDIR /tf-knugs

COPY requirements.txt requirements.txt

RUN /usr/bin/python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8888

ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
