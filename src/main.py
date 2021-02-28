#! /usr/bin/env python3

import hotshotpy
import json
import os
import sys
import time

from hotshotpy.observer import start_observer
from pathlib import Path
from hotshotpy.version import __version__
from hotshotpy.web_server import start_web_server


if __name__ == '__main__':
    #for k, v in sorted(os.environ.items()):
    #    print(f"k:{k}", v)

    print(f"HotshotPy version {__version__}")

    config_file = Path(hotshotpy.config_file())
    if not config_file.is_file():
        user_config = {
            "screenshots_dir": hotshotpy.common("screenshots/"),
            "webserver_port": 8765
        }
        with open(hotshotpy.config_file(), "w") as config_file:
            print(json.dumps(user_config, indent=4,
                             sort_keys=True), file=config_file)

        p = Path(user_config['screenshots_dir'])
        if not p.exists():
            p.mkdir(exist_ok=True)

        print()
        print(f"You didn't have a config file.")
        print(f"One was generated at {hotshotpy.config_file()}")
        print(f"Please review and edit it, then rerun this program.")
        sys.exit()
    else:
        with open(hotshotpy.config_file(), "r") as json_file:
            hotshotpy.user_config = json.load(json_file)

    print(f"SQLite3 database : {hotshotpy.config.db_file()}")
    print(f"Screenshots directory : {hotshotpy.user_config['screenshots_dir']}")
    print(f"Web server port : {hotshotpy.user_config['webserver_port']}")

    p = Path(hotshotpy.config.db_file())
    if not p.exists():
        print(f"Database file {hotshotpy.config.db_file()} does not exist.")
        sys.exit()

    p = Path(hotshotpy.user_config['screenshots_dir'])
    if not p.exists():
        print(f"Screenshots directory {hotshotpy.user_config['screenshots_dir']} does not exist.")
        sys.exit()
        
    observer = start_observer(hotshotpy.user_config['screenshots_dir'])
    web_server = start_web_server(hotshotpy.user_config['webserver_port'])

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
