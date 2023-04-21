# syntax=docker/dockerfile:1

# Use an official Python runtime as a parent image
FROM python:slim-buster

# Add non-root user
RUN addgroup --system psiuser && adduser --system --group psiuser

# Set the user to psiuser
USER psiuser

# Set the working directory to /home/psiuser
WORKDIR /home/psiuser

# Copy all files into the container at /home/psiuser
COPY . /home/psiuser

# Add /home/psiuser/.local/bin to environment variables
ENV PATH=$PATH:/home/psiuser/.local/bin

# Install libraries
RUN pip install --user -U pip
RUN pip install --user --no-cache-dir -r requirements.txt
RUN pip install --user --no-cache-dir gunicorn Flask-Limiter[redis]==3.3.0

# Expose port 80 for gunicorn
EXPOSE 80/tcp

# Start the application with gunicorn
CMD [ "gunicorn", "-b", "0.0.0.0:80", "wsgi:app", "-w", "5" ]

# HEALTHCHECK for index page every 5 minutes
HEALTHCHECK --interval=5m CMD curl -f http://localhost:80/ || exit 1
