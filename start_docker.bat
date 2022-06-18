docker build -t mqbot .
docker run -d  --name mqbot mqbot -v token.txt:/app/token.txt