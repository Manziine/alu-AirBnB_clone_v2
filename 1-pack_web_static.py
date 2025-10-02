#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    create the archive file with the contents of the web_static folder
    and return the archive path if the archive has been correctly generated
    otherwise return None
    """
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "web_static_{}.tgz".format(datetime_str)
    try:
        local('mkdir -p versions')
        local('tar -cvzf versions/{} web_static'.format(file_name))
        return "versions/{}".format(file_name)
    except:
        return None
