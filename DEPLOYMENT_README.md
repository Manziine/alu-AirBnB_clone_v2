# AirBnB Clone v2 - Deployment Documentation

## 📋 Project Overview

This project implements automated deployment of the AirBnB web_static content to web servers using Fabric and Docker.

## 🎯 Learning Objectives

- ✅ What is Fabric and how to use it
- ✅ How to deploy code to servers easily  
- ✅ What is a tgz archive
- ✅ How to execute Fabric commands locally and remotely
- ✅ How to transfer files with Fabric
- ✅ How to manage Nginx configuration
- ✅ Difference between root and alias in Nginx configuration

## 📁 Project Files

### Required Files (Fabric Deployment)

1. **`0-setup_web_static.sh`** - Bash script to prepare web servers
   - Installs Nginx
   - Creates directory structure (`/data/web_static/`)
   - Sets up symbolic links
   - Configures Nginx with `alias` directive

2. **`1-pack_web_static.py`** - Fabric script to create .tgz archive
   - Function: `do_pack()`
   - Creates timestamped archive: `web_static_<YYYYMMDDHHMMSS>.tgz`
   - Stores in `versions/` directory

3. **`2-do_deploy_web_static.py`** - Fabric script to deploy archive
   - Function: `do_deploy(archive_path)`
   - Uploads archive to `/tmp/` on servers
   - Extracts to `/data/web_static/releases/`
   - Updates symbolic link `/data/web_static/current`

4. **`3-deploy_web_static.py`** - Full deployment script
   - Function: `deploy()`
   - Combines `do_pack()` and `do_deploy()`
   - Complete end-to-end deployment

### Bonus Files (Docker Deployment)

5. **`Dockerfile`** - Container definition for web servers
6. **`docker-compose.yml`** - Multi-container orchestration
7. **`haproxy.cfg`** - Load balancer configuration
8. **`fabfile.py`** - Python 3.13 compatible deployment script

## 🚀 Usage

### Method 1: Fabric Deployment (Original Assignment)

```bash
# Pack web_static into archive
fab -f 1-pack_web_static.py do_pack

# Deploy specific archive to servers
fab -f 2-do_deploy_web_static.py do_deploy:archive_path=versions/web_static_20170315003959.tgz -i ~/.ssh/my_key -u ubuntu

# Full deployment (pack + deploy)
fab -f 3-deploy_web_static.py deploy -i ~/.ssh/my_key -u ubuntu
```

### Method 2: Python 3.13 Compatible Script

```bash
# Create archive
python fabfile.py pack

# Full deployment (requires SSH key)
python fabfile.py deploy -i ~/.ssh/my_key
```

### Method 3: Docker Deployment (Modern Approach)

```bash
# Build and start all containers
docker-compose up -d --build

# Access points:
# - Load Balancer: http://localhost:8080
# - Web Server 01: http://localhost:8081
# - Web Server 02: http://localhost:8082
# - HAProxy Stats: http://localhost:8404/stats
```

## 🏗️ Architecture

### Production Architecture (Fabric)
```
Developer Machine
    ↓ (Fabric/SSH)
┌───────────────┐
│  Load Balancer│
│   (HAProxy)   │
└───────┬───────┘
        │
    ┌───┴───┐
    ↓       ↓
┌─────┐ ┌─────┐
│Web-01│ │Web-02│
│Nginx │ │Nginx │
└─────┘ └─────┘
```

### Docker Architecture (Local Testing)
```
Docker Host
    ↓
┌──────────────┐
│ HAProxy LB   │ :8080
└──────┬───────┘
       │
   ┌───┴───┐
   ↓       ↓
┌──────┐ ┌──────┐
│Web-01│ │Web-02│
│:8081 │ │:8082 │
└──────┘ └──────┘
```

## 📝 Deployment Process

### Step 1: Prepare Servers (One-time setup)
```bash
# Run on each web server
sudo ./0-setup_web_static.sh
```

This creates:
- `/data/web_static/releases/test/` - Test deployment
- `/data/web_static/shared/` - Shared resources
- `/data/web_static/current` → symlink to active release
- Nginx configuration for `/hbnb_static` location

### Step 2: Pack Application
```bash
python fabfile.py pack
```

Creates: `versions/web_static_YYYYMMDDHHMMSS.tgz`

### Step 3: Deploy to Servers
```bash
python fabfile.py deploy -i ~/.ssh/your_key
```

Process:
1. Creates archive locally
2. Uploads to `/tmp/` on each server
3. Extracts to `/data/web_static/releases/<timestamp>/`
4. Updates `/data/web_static/current` symlink
5. Nginx serves from new version

## 🧪 Testing

### Test Individual Components

```bash
# Test archive creation
python fabfile.py pack
ls -lh versions/

# Test Nginx configuration
curl http://your-server-ip/hbnb_static/0-index.html

# Test load balancing (Docker)
for i in {1..10}; do 
    curl -I http://localhost:8080/hbnb_static/0-index.html 2>&1 | grep "x-served-by"
done
```

### Expected Output

The page should display:
- Red header bar at top
- White body in middle
- Green footer with "Holberton School" text

## 🔧 Troubleshooting

### Fabric Compatibility Issues (Python 3.10+)

**Problem:** `ImportError: cannot import name 'Mapping' from 'collections'`

**Solution:** Use `fabfile.py` instead of Fabric3:
```bash
python fabfile.py pack
python fabfile.py deploy -i ~/.ssh/key
```

### SSH Connection Issues

**Problem:** Permission denied or connection refused

**Solutions:**
1. Verify SSH key permissions: `chmod 600 ~/.ssh/your_key`
2. Test SSH connection: `ssh -i ~/.ssh/your_key ubuntu@server-ip`
3. Check server IPs in scripts match your servers

### Nginx Not Serving Content

**Problem:** 404 errors on `/hbnb_static/`

**Solutions:**
1. Check symlink: `ls -la /data/web_static/current`
2. Verify Nginx config: `sudo nginx -t`
3. Restart Nginx: `sudo service nginx restart`

## 📊 Project Structure

```
alu-AirBnB_clone_v2/
├── 0-setup_web_static.sh          # Server setup script
├── 1-pack_web_static.py            # Archive creation (Fabric)
├── 2-do_deploy_web_static.py       # Deployment script (Fabric)
├── 3-deploy_web_static.py          # Full deployment (Fabric)
├── fabfile.py                      # Python 3.13 compatible version
├── Dockerfile                      # Docker web server image
├── docker-compose.yml              # Multi-container setup
├── haproxy.cfg                     # Load balancer config
├── web_static/                     # Static HTML/CSS files
│   ├── 0-index.html
│   ├── 1-index.html
│   ├── ...
│   ├── images/
│   └── styles/
└── versions/                       # Generated archives
    └── web_static_*.tgz
```

## ✅ Checklist

- [x] Bash script creates proper directory structure
- [x] Nginx configured with `alias` directive
- [x] Archive creation with timestamp naming
- [x] Deployment to multiple servers
- [x] Symbolic link management
- [x] Load balancing with HAProxy
- [x] Docker containerization (bonus)
- [x] Python 3.13 compatibility (bonus)

## 🎓 Key Concepts Demonstrated

1. **Infrastructure as Code** - Automated server setup
2. **Continuous Deployment** - Scripted deployment process
3. **Load Balancing** - Traffic distribution across servers
4. **Containerization** - Docker-based deployment
5. **Version Control** - Timestamped releases
6. **Zero-Downtime Deployment** - Symbolic link switching

## 👤 Author

**Arnold Manzi**
- GitHub: [@Manziine](https://github.com/Manziine)
- Project: ALU Software Engineering Program

## 📅 Project Timeline

- **Created:** October 2025
- **Technologies:** Python, Fabric, Docker, Nginx, HAProxy
- **Status:** ✅ Complete

---

**Note:** This project demonstrates both traditional Fabric deployment and modern Docker containerization approaches, providing flexibility for different deployment scenarios.
