FROM python:3

# Copy . to /app/
COPY . /app/
WORKDIR /app/

# Install requirements from requirements.txt
RUN pip install -r requirements.txt

# Specify environment variables
ENV PYTHONUNBUFFERED=0

# Target Creeper#1268 by default :3
ENV TARGET_ID=155792332703137792
ENV TOKEN=invalidtoken

# Join/leave delay
ENV JOIN_DELAY=0
ENV LEAVE_DELAY=0

# Run the app
CMD ["python", "app.py"]