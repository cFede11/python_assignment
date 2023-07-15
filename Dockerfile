FROM python:3.9

WORKDIR /app

# Set the environment variable for the Alpha Vantage API key
ENV AV_API_KEY="128S2A8V57C2W8UP"

COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy all files from the current directory to the working directory
COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000
