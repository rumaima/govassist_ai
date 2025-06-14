FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port for Gradio
EXPOSE 7860

# Run the app
CMD ["python", "frontend/frontend_app.py"]