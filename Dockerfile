# No changes are needed here.
FROM python:3.11-slim
WORKDIR /app
COPY server.py .
EXPOSE 3000
CMD ["python3", "server.py"]
