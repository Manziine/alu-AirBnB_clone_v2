#!/usr/bin/python3
"""
Fabfile for AirBnB deployment - Python 3.13 compatible version
This uses direct paramiko instead of Fabric for compatibility
"""
import os
import sys
from datetime import datetime
import subprocess
import paramiko

# Server configuration - UPDATE THESE WITH YOUR SERVER IPS
SERVERS = [
    {'host': '34.74.23.57', 'user': 'ubuntu'},
    {'host': '35.196.161.89', 'user': 'ubuntu'}
]

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    
    Returns:
        Archive path if successfully generated, None otherwise.
    """
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "web_static_{}.tgz".format(datetime_str)
    
    try:
        if not os.path.exists('versions'):
            os.makedirs('versions')
            print("Created versions directory")
        
        cmd = 'tar -czf versions/{} web_static'.format(file_name)
        print(f"Packing web_static to versions/{file_name}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            archive_path = "versions/{}".format(file_name)
            size = os.path.getsize(archive_path)
            print(f"web_static packed: {archive_path} -> {size} Bytes")
            return archive_path
        else:
            print(f"Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def do_deploy(archive_path, ssh_key_path=None):
    """
    Distributes an archive to web servers.
    
    Args:
        archive_path: Path to the archive file to deploy
        ssh_key_path: Path to SSH private key (optional)
        
    Returns:
        True if all operations succeed, False otherwise
    """
    if not os.path.exists(archive_path):
        print(f"[ERROR] Archive not found: {archive_path}")
        return False
    
    file_name = os.path.basename(archive_path)
    file_name_noext = file_name.replace('.tgz', '')
    
    for server in SERVERS:
        try:
            print(f"\n[{server['host']}] Executing task 'do_deploy'")
            
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            connect_kwargs = {
                'hostname': server['host'],
                'username': server['user']
            }
            
            if ssh_key_path and os.path.exists(ssh_key_path):
                connect_kwargs['key_filename'] = ssh_key_path
            
            ssh.connect(**connect_kwargs)
            
            # Upload archive
            print(f"[{server['host']}] put: {archive_path} -> /tmp/{file_name}")
            sftp = ssh.open_sftp()
            sftp.put(archive_path, f'/tmp/{file_name}')
            sftp.close()
            
            # Execute deployment commands
            commands = [
                f'mkdir -p /data/web_static/releases/{file_name_noext}/',
                f'tar -xzf /tmp/{file_name} -C /data/web_static/releases/{file_name_noext}/',
                f'rm /tmp/{file_name}',
                f'mv /data/web_static/releases/{file_name_noext}/web_static/* /data/web_static/releases/{file_name_noext}/',
                f'rm -rf /data/web_static/releases/{file_name_noext}/web_static',
                f'rm -rf /data/web_static/current',
                f'ln -s /data/web_static/releases/{file_name_noext}/ /data/web_static/current'
            ]
            
            for cmd in commands:
                print(f"[{server['host']}] run: {cmd}")
                stdin, stdout, stderr = ssh.exec_command(cmd)
                exit_status = stdout.channel.recv_exit_status()
                if exit_status != 0:
                    error = stderr.read().decode()
                    print(f"[{server['host']}] Warning: {error}")
            
            print(f"New version deployed!")
            ssh.close()
            
        except Exception as e:
            print(f"[{server['host']}] Error: {e}")
            return False
    
    print("\nDone.")
    return True

def deploy(ssh_key_path=None):
    """
    Creates and distributes an archive to web servers.
    
    Args:
        ssh_key_path: Path to SSH private key (optional)
        
    Returns:
        True if deployment succeeds, False otherwise
    """
    print("=" * 60)
    print("STARTING FULL DEPLOYMENT")
    print("=" * 60)
    
    archive_path = do_pack()
    if not archive_path:
        print("\n❌ Failed to create archive")
        return False
    
    result = do_deploy(archive_path, ssh_key_path)
    if result:
        print("\n" + "=" * 60)
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("=" * 60)
    else:
        print("\n❌ DEPLOYMENT FAILED")
    
    return result

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Deploy AirBnB web_static')
    parser.add_argument('command', choices=['pack', 'deploy'], 
                       help='Command to execute: pack or deploy')
    parser.add_argument('--archive', help='Archive path for deploy command')
    parser.add_argument('-i', '--key', help='SSH private key path')
    
    args = parser.parse_args()
    
    if args.command == 'pack':
        result = do_pack()
        sys.exit(0 if result else 1)
    elif args.command == 'deploy':
        if args.archive:
            result = do_deploy(args.archive, args.key)
        else:
            result = deploy(args.key)
        sys.exit(0 if result else 1)
