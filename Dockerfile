# syntax=docker/dockerfile:1

# Use an official Python runtime as a parent image
FROM python:slim

# Add non-root user
RUN addgroup --system psiuser && adduser --system --group psiuser

USER psiuser

# update and installl netcat
RUN apt-get update && apt-get upgrade -y

# Set the working directory to /home/psiapp
WORKDIR /home/psiapp

# Copy all files into the container at /home/psiapp
COPY . /home/psiapp

RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn Flask-Limiter[redis]==3.3.0

# Expose port 5000 for gunicorn
EXPOSE 5000/tcp

# Start the application with gunicorn
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5000", "wsgi:app", "-w" ]

# Easily override workers in: docker run <image_name> <workers>
CMD [ "5" ]

# HEALTHCHECK for index page every 5 minutes
HEALTHCHECK --interval=5m CMD curl -f http://localhost:5000/ || exit 1
