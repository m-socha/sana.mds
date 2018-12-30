FROM ubuntu:14.04
COPY ./docker /docker_install
RUN apt-get update
ENV DEBIAN_FRONTEND=noninteractive
RUN echo "mysql-server-5.5 mysql-server/root_password password root" | sudo debconf-set-selections
RUN echo "mysql-server-5.5 mysql-server/root_password_again password root" | sudo debconf-set-selections
RUN apt-get -y install vim
RUN apt-get -y install apache2         
RUN apt-get -y install mysql-server    
RUN apt-get -y install libapache2-mod-wsgi         
RUN apt-get -y install libapache2-mod-jk           
RUN apt-get -y install python-cjson                
RUN apt-get -y install python-django
RUN apt-get -y install python-mysqldb             
RUN apt-get -y install python-django-piston                    
RUN apt-get -y install python-libxml2              
RUN apt-get -y install python-lxml                 
RUN apt-get -y install python-django-extensions    
RUN apt-get -y install python-django-extra-views   
RUN apt-get -y install python-imaging    
RUN apt-get -y install python-pip         
RUN apt-get -y install sqlite3                     
RUN apt-get -y install javascript-common           
RUN apt-get -y install libjs-jquery-ui             
RUN apt-get -y install libjs-jquery-timepicker
RUN printf 'export MDS_DIR=/opt/sana/sana.mds' >> /etc/apache2/envvars
ENV MDS_DIR=/opt/sana/sana.mds
RUN printf "django\ndjango\n\n\n\n\n\nY\n" | adduser django
RUN usermod -a -G django www-data
RUN mkdir -p /opt/sana/cache                \
    /opt/sana/sana.mds/cache/media      \
    /opt/sana/sana.mds/cache/static     \
    /opt/sana/sana.mds/cache/db
RUN a2enmod wsgi
RUN cp /docker_install/.my.cnf ~/.my.cnf
RUN service mysql restart && mysql < /docker_install/initialize_db.sql
ENTRYPOINT ["tail", "-f", "/dev/null"]