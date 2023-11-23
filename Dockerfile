# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY Backend/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local Backend directory to the working directory
COPY Backend/ .

# Expose port 8000
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
