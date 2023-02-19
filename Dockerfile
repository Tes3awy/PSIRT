# syntax=docker/dockerfile:1

FROM python:3.11.2-alpine
WORKDIR /psiapp
COPY . .
RUN python3 -m pip install -U wheel pip setuptools
RUN python3 -m pip install -r requirements.txt
RUN echo "All Python requirements were successfully installed"
EXPOSE 8080
CMD ["gunicorn", "--workers", "12", "--bind", "0.0.0.0:8080", "wsgi:app", "--log-level", "info", "--access-logfile=-"]
