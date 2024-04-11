cp /data/vol0/minikube/.minikube/profiles/minikube/client.key ~/Documents/nginx-docker/assets/
cp /data/vol0/minikube/.minikube/profiles/minikube/client.crt ~/Documents/nginx-docker/assets/
cp /data/vol0/minikube/.minikube/ca.crt ~/Documents/nginx-docker/assets/

docker rmi nginx-dev-cluster; docker build -t nginx-dev-cluster .

# docker run -d --memory="500m" --memory-reservation="256m" --cpus="0.25" --name nginx-dev-cluster -p 443:443 -p 80:80 --network=minikube nginx-dev-cluster
