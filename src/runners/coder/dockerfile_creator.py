import os
import logging

# Create a path to the /examples directory, combining the current working directory "examples" folder
script_directory = os.path.join(os.getcwd(), "examples")

# Path where the Dockerfile will be created
dockerfile_path = os.path.join(script_directory, "Dockerfile")

# Dockerfile content
dockerfile_content = '''
FROM python:latest
WORKDIR /app
COPY . /app
VOLUME ["/app"]
CMD ["python", "{script_name}"]
'''.format(script_name=os.path.basename(script_directory))

# Write the Dockerfile
with open(dockerfile_path, "w") as dockerfile:
    dockerfile.write(dockerfile_content)

logging.debug("Dockerfile created successfully at: " + dockerfile_path)