# Update and Install requirements
apt-get update && apt-get upgrade -y tzdata
apt-get install -y python3-pip python3-dev python3-venv python3-setuptools nginx redis supervisor git

# Create Python Virtual Environment and install requirements, Gunicorn, and Flask-Limiter
python3 -m venv /home/vagrant/app/venv
source /home/vagrant/app/venv/bin/activate
python3 -m pip install --no-cache-dir --upgrade pip setuptools
python3 -m pip install --no-cache-dir -r /home/vagrant/app/requirements.txt gunicorn Flask-Limiter[redis]==3.3.0

# Configure Nginx
unlink /etc/nginx/sites-enabled/default
cp /home/vagrant/app/nginx.conf /etc/nginx/sites-enabled/

# Start the application
nginx -s reload

# Configure supervisor
mkdir /var/log/psiapp
touch /var/log/psiapp/psiapp.out.log
touch /var/log/psiapp/psiapp.err.log
cp /home/vagrant/app/supervisor.conf /etc/supervisor/conf.d/
supervisorctl reload

# Check VM's assigned IP Address
hostname -I