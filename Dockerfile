FROM ubuntu:16.04
RUN apt-get update
RUN apt-get -y install apt-utils
RUN apt-get -y install build-essential
RUN apt-get -y install python
RUN apt-get -y install python-dev
RUN apt-get -y install python-setuptools
RUN apt-get -y install graphviz
RUN apt-get -y install python-pip
ADD test.py /
ADD grafo.py /
ADD ast_walker.py /
ADD foo.py /
ADD no.py /
RUN pip install coverage
RUN pip install ast
RUN pip install graphviz
RUN python ./test.py
