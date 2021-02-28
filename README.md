# HotshotPy

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/hotshotpy)


This tool helps managing Hotshot Racing championships.

(More description to come)

## First run

The first time `hotshotpy` is run, it will create a default configuration file (`${HOME}/snap/hotshotpy/common/hotshotpy.conf`). Please review and edit this file.

In particular, check the `screenshot_dirs` entry, and make sure it points to the directory where `steam` put the screen captures. This directory needs to be available to the snap, so its possible locations are limited. By default, it will be `${HOME}/snap/hotshotpy/common/screenshots` and this directory will be automatically created if it does not exist.

To regenerate the default configuration file, just delete `${HOME}/snap/hotshotpy/common/hotshotpy.conf` and start `hotshotpy`.

## Database

To function properly, a SQLite3 database is needed. At the time of writing, the easiest way to get a database with some historical values, is to clone the [hotshotpydb](http://github.com/ymauray/hotshotpydb) repository on github :

```
cd ${HOME}/snap/hotshotpy/common
git clone http://github.com/ymauray/hotshotpydb.git
```

## Backend

At the time of writing, there is only a parial webpage available, at `http://localhost:8765/backend/results.html` (or whatever port is specified in the configuration file).

The only operation available is to change the active event, by clicking the `save` icon on the right of the events dropdown.
