FROM tesseractshadow/tesseract4re
WORKDIR /app

# Copy the project files to the working directory
COPY . .

# Set the command to run the application
CMD ["python", "main.py"]

