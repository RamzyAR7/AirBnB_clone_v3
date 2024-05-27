#!/usr/bin/python3
"""To compress webstatic"""
import datetime
from fabric.operations import local
from os.path import isdir


def do_pack():
    """Packs webstatic into tgz"""
    try:
        result = str(local("file versions"))
        print(result)
        print(len(result))
        if isdir("versions") is False:
            local("mkdir versions")
        date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = "versions/web_static_{}.tgz".format(date)
        local("tar -czvf {} web_static".format(file_path))
        return file_path
    except Exception:
        return None
