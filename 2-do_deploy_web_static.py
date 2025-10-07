#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
using the function do_deploy
"""
from fabric.api import env, run, put
import os.path


env.hosts = ['34.74.23.57', '35.196.161.89']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path: Path to the archive file to deploy

    Returns:
        True if all operations succeed, False otherwise
    """
    if not os.path.exists(archive_path):
        return False
    
    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')
        
        # Extract filename from path
        file_name = os.path.basename(archive_path)
        # Remove .tgz extension to get folder name
        file_name_noext = file_name.replace('.tgz', '')
        
        # Create the release directory
        run('mkdir -p /data/web_static/releases/{}/'.format(file_name_noext))
        
        # Uncompress the archive to the release directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(file_name, file_name_noext))
        
        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_name))
        
        # Move contents from web_static subdirectory to release directory
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(file_name_noext, file_name_noext))
        
        # Remove the now-empty web_static subdirectory
        run('rm -rf /data/web_static/releases/{}/web_static'.format(file_name_noext))
        
        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')
        
        # Create new symbolic link to the new release
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(file_name_noext))
        
        print("New version deployed!")
        return True
        
    except Exception:
        return False
