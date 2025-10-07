#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
using the function do_deploy
"""
from fabric.api import env, run, put
import os

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
