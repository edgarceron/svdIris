# Dockerfile

FROM python:3.7-buster

# install nginx
RUN apt-get update && apt-get install unzip -y && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/datairis
COPY requirements.txt start-server.sh /opt/app/
COPY .pip_cache /opt/app/pip_cache/
RUN mkdir -p /opt/app/extra
RUN cd /opt/app/ \  
    && git clone https://github.com/edgarceron/svdIris
WORKDIR /opt/app
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN chown -R www-data:www-data /opt/app
RUN cd /opt/app/svdIris && unzip MMU-Iris-Database.zip -d /opt/app/datairis
RUN cd /opt/app/svdIris && python manage.py import_iris /opt/app/datairis/MMU-Iris-Database
RUN cd /opt/app/svdIris && python manage.py collectstatic --noinput

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]