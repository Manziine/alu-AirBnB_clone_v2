#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py) that creates and
distributes an archive to your web servers, using the function deploy
"""
from fabric.api import local, env, run, put
from datetime import datetime
import os

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
        local('mkdir -p versions')
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
        put(archive_path, '/tmp/')
        file_name = archive_path.split('/')[-1]
        file_name_noext = file_name.split('.')[0]
        new_folder = '/data/web_static/releases/' + file_name_noext + '/'
        run('sudo mkdir -p {}'.format(new_folder))
        run('sudo tar -xzf /tmp/{} -C {}'.format(file_name, new_folder))
        run('sudo rm /tmp/{}'.format(file_name))
        run('sudo mv {}web_static/* {}'.format(new_folder, new_folder))
        run('sudo rm -rf {}web_static'.format(new_folder))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(new_folder))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Creates and distributes an archive to web servers.

    Returns:
        True if deployment succeeds, False otherwise
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
