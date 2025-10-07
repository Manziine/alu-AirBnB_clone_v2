# AirBnB Clone v2 - Docker Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Docker Compose installed

### Deploy the Application

```bash
# Build and start all containers
docker-compose up -d --build

# Check running containers
docker ps

# View logs
docker-compose logs -f
```

### Access Points

- **Load Balancer (HAProxy)**: http://localhost:8080
- **Web Server 01**: http://localhost:8081
- **Web Server 02**: http://localhost:8082
- **HAProxy Stats**: http://localhost:8404/stats

### Test Load Balancing

```bash
# Make multiple requests to see round-robin in action
curl http://localhost:8080/hbnb_static/0-index.html
curl http://localhost:8080/hbnb_static/0-index.html
curl http://localhost:8080/hbnb_static/0-index.html
```

### Architecture

```
                    ┌─────────────────┐
                    │   HAProxy LB    │
                    │  (Port 8080)    │
                    └────────┬────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
         ┌──────▼──────┐          ┌──────▼──────┐
         │   Web-01    │          │   Web-02    │
         │ (Port 8081) │          │ (Port 8082) │
         │   Nginx     │          │   Nginx     │
         └─────────────┘          └─────────────┘
```

## 📦 What Was Created

1. **Dockerfile** - Nginx container serving web_static
2. **docker-compose.yml** - Orchestrates 2 web servers + HAProxy
3. **haproxy.cfg** - Load balancer configuration (round-robin)
4. **.dockerignore** - Optimizes Docker build

## 🛠️ Management Commands

```bash
# Stop all containers
docker-compose down

# Rebuild after changes
docker-compose up -d --build

# View container logs
docker-compose logs web01
docker-compose logs web02
docker-compose logs haproxy

# Restart a specific service
docker-compose restart web01

# Remove everything (including volumes)
docker-compose down -v
```

## 🧪 Testing

1. **Test individual servers:**
   ```bash
   curl http://localhost:8081/hbnb_static/0-index.html
   curl http://localhost:8082/hbnb_static/0-index.html
   ```

2. **Test load balancer:**
   ```bash
   for i in {1..10}; do curl -I http://localhost:8080/hbnb_static/0-index.html 2>&1 | grep "X-Served-By"; done
   ```

3. **Monitor HAProxy stats:**
   - Open browser: http://localhost:8404/stats

## 📝 Notes

- This setup simulates the production environment locally
- HAProxy uses round-robin algorithm to distribute traffic
- Each request alternates between web-01 and web-02
- All containers are on the same Docker network for communication
