# syntax=docker/dockerfile:1

# Use an official Python runtime as a parent image
FROM python:slim

RUN useradd psiuser

# Set the working directory to /home/psiapp
WORKDIR /home/psiapp

# Copy all files into the container at /home/psiapp
COPY . /home/psiapp

RUN pip install wheel
RUN pip install -r requirements.txt
RUN pip install gunicorn Flask-Limiter[redis]==3.3.0

# Expose port 5000 for gunicorn
EXPOSE 5000

# Start the application with gunicorn
CMD ["gunicorn", "-w", "5", "-b", "0.0.0.0:5000", "wsgi:app", "--access-logfile=-"]
