# Dockerfile for AirBnB web_static deployment
FROM nginx:alpine

# Install necessary packages
RUN apk add --no-cache bash

# Create directory structure
RUN mkdir -p /data/web_static/releases/test/ && \
    mkdir -p /data/web_static/shared/

# Copy web_static content
COPY web_static /data/web_static/releases/test/web_static/

# Create symbolic link
RUN ln -sf /data/web_static/releases/test/web_static /data/web_static/current

# Configure Nginx
COPY <<EOF /etc/nginx/conf.d/default.conf
server {
    listen 80;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
        autoindex off;
    }

    location / {
        root /data/web_static/current;
        index index.html 0-index.html;
    }
}
EOF

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
