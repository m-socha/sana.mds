#!/usr/bin/env bash
rm /opt/sana/sana.mds/mds /var/www/html/mds
ln -s /sana.mds/src/mds /opt/sana/sana.mds/mds
rm /etc/apache2/conf-available/mds.conf
cp /sana.mds/include/mds/apache2/conf-available/mds.conf /etc/apache2/conf-available/
a2enconf mds
rm /sana.mds/src/mds/settings.py /sana.mds/src/mds/local_settings.py
cp /sana.mds/src/mds/settings.py.tmpl /sana.mds/src/mds/settings.py
echo "ALLOWED_HOSTS=['*']" >> /sana.mds/src/mds/settings.py
echo "STATICFILES_DIRS=['/sana.mds/src/mds/web/static']" >> /sana.mds/src/mds/settings.py
sed -i "s/\*\*\*\*\*\*\*\*/mds/g" /sana.mds/src/mds/settings.py
sed -i "s/'HOST': ''/'HOST': 'localhost'/g" /sana.mds/src/mds/settings.py
sed -i "s/'PORT': ''/'PORT': '3306'/g" /sana.mds/src/mds/settings.py
cp /sana.mds/src/mds/local_settings.py.tmpl /sana.mds/src/mds/local_settings.py
service mysql restart
python /sana.mds/src/manage.py syncdb --noinput
python /sana.mds/src/manage.py collectstatic --noinput
ln -sf /opt/sana/sana.mds/mds /var/www/html/mds
service apache2 restart