FROM python:3.9-slim

# Install required packages including Autogen
RUN pip install autogen

# Copy your agent code into the container
COPY . /app
WORKDIR /app

# Set the container’s entrypoint (adjust as needed)
CMD ["python", "run_agent.py"]
