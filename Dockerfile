FROM tesseractshadow/tesseract4re
WORKDIR /app

# Copy the project files to the working directory
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Set the command to run the application
CMD ["python", "main.py"]

