#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""


from os.path import exists
from fabric.api import put, run, env
from fabric import exceptions
env.hosts = ["54.173.91.227", "3.85.1.149"]


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run(f'mkdir -p {path}{no_ext}/')
        run(f'tar -xzf /tmp/{file_n} -C {path}{no_ext}/')
        run(f'rm /tmp/{file_n}')
        run(f'mv {path}{no_ext}/web_static/* {path}{no_ext}/')
        run(f'rm -rf {path}{no_ext}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {path}{no_ext}/ /data/web_static/current')
        run('service nginx restart')
        return True
    except exceptions.CommandTimeout:
        return False
    except exceptions.NetworkError:
        return False
