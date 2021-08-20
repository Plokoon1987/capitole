docker stop myapp; docker rm myapp

docker rmi -f froylan/capitole

docker build -t froylan/capitole .

docker run -d -p 5000:5000 --name myapp froylan/capitole
