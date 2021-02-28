import os

user_config = dict()

def common(subpath: None):
    common = os.getenv("SNAP_USER_COMMON")
    if common is None:
        common = "/tmp"

    if subpath is None:
        return common
    else:
        return f"{common}/{subpath}"


def www_root():
    root = os.getenv("SNAP")
    if root is None:
        root = os.path.dirname(os.path.dirname(__file__))
    return f'{root}/www-root'


def db_file():
    return common("hotshotpydb/sqlite3.db")


def config_file():
    return common("hotshotpy.conf")
