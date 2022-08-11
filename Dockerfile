FROM python:3

# Copy . to /app/
COPY . /app/
WORKDIR /app/

# Update apt
RUN apt update

# Install ffmpeg
RUN apt install ffmpeg -y

# Install requirements from requirements.txt
RUN pip install -r requirements.txt

# Install youtube-dl
RUN pip install youtube-dl

# Download rick roll to `audio`
RUN youtube-dl -x --audio-format mp3 -o 'audio.out' https://www.youtube.com/watch?v=dQw4w9WgXcQ
RUN mv audio.mp3 audio

# Specify environment variables
ENV PYTHONUNBUFFERED=0

# Target Creeper#1268 by default :3
ENV TARGET_ID=155792332703137792
ENV TOKEN=invalidtoken

# Join/leave delay
ENV JOIN_DELAY=0
ENV LEAVE_DELAY=0

# Audio
ENV PLAY_AUDIO=false

# Run the app
CMD ["python", "app.py"]