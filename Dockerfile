FROM python:3.10-buster
RUN /usr/local/bin/python -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple
RUN mkdir /code
WORKDIR /code
COPY requirements-prd.txt /code/
RUN pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements-prd.txt
COPY . /code/
RUN pip install djangorestframework
RUN pip install django-filter
RUN pip install django-debug-toolbar
#RUN pip install python-memcached
RUN pip install pymemcache