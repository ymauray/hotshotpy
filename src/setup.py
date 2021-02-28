import setuptools

from hotshotpy.version import __version__

setuptools.setup(
    name="hotshotpy",
    version=__version__,
    author="Yannick Mauray",
    author_email="yannick@frenchguy.ch",
    description="A simple tool to help manage Hotshot Racing championships",
    scripts=[
        "main.py",
    ],
    packages=[
        "controllers",
        "hotshotpy",
    ]
)
