cp /data/vol0/minikube/.minikube/profiles/minikube/client.key ~/Documents/nginx-docker/assets/
cp /data/vol0/minikube/.minikube/profiles/minikube/client.crt ~/Documents/nginx-docker/assets/
cp /data/vol0/minikube/.minikube/ca.crt ~/Documents/nginx-docker/assets/

docker rmi nginx-dev-cluster; docker build -t nginx-dev-cluster .


