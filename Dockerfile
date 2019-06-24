FROM python:3.7

# Create Application Source Code Directory
RUN mkdir -p /corere

# Setting Home Directory for Containers
WORKDIR /corere

# Installing Python Dependencies
COPY requirements.txt /corere
RUN pip install --no-cache-dir -r requirements.txt

# Copying src code to Container
COPY . /corere/

# Application Environment variables
ENV APP_ENV development

# Exposing Ports
EXPOSE 5000

# Setting Persistent data
VOLUME ["/app-data"]

# Running Python Application
CMD ["./run.sh"]
