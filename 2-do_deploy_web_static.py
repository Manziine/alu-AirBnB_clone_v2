#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
using the function do_deploy
"""
from fabric.api import env, run, put, local
import os.path
from datetime import datetime


env.hosts = ['34.74.23.57', '35.196.161.89']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        Archive path if successfully generated, None otherwise.
    """
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "web_static_{}.tgz".format(datetime_str)
    try:
        # Create versions directory if it doesn't exist (cross-platform)
        if not os.path.exists('versions'):
            os.makedirs('versions')
        
        # Use tar command to create archive
        local('tar -cvzf versions/{} web_static'.format(file_name))
        return "versions/{}".format(file_name)
    except Exception:
        return None


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
        
        # Extract filename from path (handle both / and \ separators)
        file_name = os.path.basename(archive_path)
        # Remove .tgz extension to get folder name
        file_name_noext = file_name.replace('.tgz', '')
        
        # Create release directory path
        release_path = '/data/web_static/releases/{}/'.format(file_name_noext)
        
        # Create the release directory
        run('mkdir -p {}'.format(release_path))
        
        # Uncompress the archive to the release directory
        run('tar -xzf /tmp/{} -C {}'.format(file_name, release_path))
        
        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_name))
        
        # Move contents from web_static subdirectory to release directory
        run('mv {}web_static/* {}'.format(release_path, release_path))
        
        # Remove the now-empty web_static subdirectory
        run('rm -rf {}web_static'.format(release_path))
        
        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')
        
        # Create new symbolic link to the new release
        run('ln -s {} /data/web_static/current'.format(release_path))
        
        print("New version deployed!")
        return True
        
    except Exception:
        return False
