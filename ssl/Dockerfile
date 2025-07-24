FROM python:3.11-slim

WORKDIR /app

# Install openssl
RUN apt-get update && apt-get install -y openssl

# Install requirements
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and script
COPY app/ ./app
COPY gencerts.sh ./gencerts.sh

# Run the script in /app
RUN sed -i 's/\r$//' gencerts.sh
RUN chmod +x ./gencerts.sh
RUN ./gencerts.sh

EXPOSE 443

CMD ["python", "app/app.py"]
