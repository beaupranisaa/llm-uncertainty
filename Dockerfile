# Use Python as the base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install Pipenv
RUN pip install pipenv

# Copy Pipenv files first to leverage Docker caching
COPY Pipfile Pipfile.lock ./

# Install dependencies globally (not in a virtual environment)
RUN pipenv install --deploy --system

# Copy the rest of the project
COPY . /app/

# Set default command to an interactive shell
CMD ["/bin/bash"]
