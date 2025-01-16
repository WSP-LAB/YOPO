docker build -t yopo-artifact ..
docker run -d --name yopo-container --gpus all -it yopo-artifact