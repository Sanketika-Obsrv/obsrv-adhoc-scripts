# Official Nginx image
FROM nginx:latest

# Copy Nginx configuration file to the container
COPY nginx.conf /etc/nginx/nginx.conf

# Copy minikube certs and password
COPY assets/client.key /etc/nginx/certs/obsrv-dev-cluster-client.key
COPY assets/client.crt /etc/nginx/certs/obsrv-dev-cluster-client.crt
COPY assets/.htpasswd /etc/nginx/.htpasswd


RUN mkdir -p /etc/nginx/cluster-certs
COPY assets/client.key /etc/nginx/cluster-certs/client.key
COPY assets/client.crt /etc/nginx/cluster-certs/client.crt
COPY assets/ca.crt /etc/nginx/cluster-certs/ca.crt
RUN chown -R nginx:nginx /etc/nginx/cluster-certs

# Expose port 80 and 443
EXPOSE 80
EXPOSE 443

