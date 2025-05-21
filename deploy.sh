#!/bin/bash
echo "Pulling latest changes..."
git pull

echo "Stopping and removing old container..."
docker stop gomail_prod && docker rm gomail_prod

echo "Rebuilding Docker image..."
docker build -t gomailbridge4bpa .

echo "Running new container..."
docker run -d --name gomail_prod -p 5050:5050 --env-file .env gomailbridge4bpa
