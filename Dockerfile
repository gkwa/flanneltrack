FROM python:slim

RUN apt-get update
RUN apt-get -y install python3 python3-dev build-essential python3-pip graphviz graphviz-dev graphviz
RUN pip install pygraphviz matplotlib networkx jinja2
