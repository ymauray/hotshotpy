import os


def common():
    common = os.getenv("SNAP_USER_COMMON")
    if common is None:
        common = "/tmp"

    return common

def www_root():
    root = os.getenv("SNAP")
    if root is None:
        root = os.path.dirname(os.path.dirname(__file__))
    return f'{root}/www-root'
