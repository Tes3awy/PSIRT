# syntax=docker/dockerfile:1

# Use an official Python runtime as a parent image
FROM python:3.10.10-alpine

# Set the working directory to /psiapp
WORKDIR /psiapp

# Copy all files into the container at /psiapp
COPY . /psiapp

# Create a virtual environment and activate it
# Although not mandatory, but you can create a venv to suppress Running pip as the 'root' user warning
# RUN python -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools

# Install needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org --default-timeout=100 -r requirements.txt

# Install gunicorn and Flask-Limiter with Redis for backend storage
RUN pip install gunicorn Flask-Limiter[redis]==3.3.0

# Expose port 5000 for gunicorn
EXPOSE 5000

# Start the application with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app", "--access-logfile=-"]
