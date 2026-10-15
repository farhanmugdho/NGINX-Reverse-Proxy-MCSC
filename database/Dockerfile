FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=samples
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password

WORKDIR /docker-entrypoint-initdb.d

COPY app.py .

EXPOSE 3306

VOLUME /var/lib/mysql