# Set the base image
$baseImage = "python:latest"

# Set the directory paths
$localCodeDirectory = "C:\Repos\DocTalk\src\runners\coder\examples"
$containerCodeDirectory = "/app"

# Create the Dockerfile content
$dockerfileContent = @"
FROM $baseImage

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get -y install build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR $containerCodeDirectory
COPY . $containerCodeDirectory

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["python", "run.py"]
"@

# Save the Dockerfile
$dockerfileContent | Out-File -FilePath "$localCodeDirectory\Dockerfile"

# Build the Docker image
docker build -t python-app "$localCodeDirectory"

# Run the Docker container
docker run -v '$localCodeDirectory:$containerCodeDirectory' python-app
