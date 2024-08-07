import os
from setuptools import setup, find_packages


rel_path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(rel_path, "sce", "globals.py")

g = {}
with open(path) as fp:
    exec(fp.read(), g)

setup(
    name=g["app_name"],
    version=g["app_version"],
    packages=find_packages(),
    include_package_data=True,
    # Note: Align this with Homebrew formula!
    python_requires=">=3.12",
    # Required third party dependencies for this application
    # Note: Also define this in the Homebrew formula via poet!
    # Note: Also import this in __init__.py!
    install_requires=[
        "argparse==1.4.0",
        "slack-sdk==3.31.0",
        "py-phone-number-fmt==2.0.0",
        "requests==2.32.3",
        "alive-progress==3.1.5"
    ],
    # Homebrew will use this to define the entry point
    # for the executable of this application.
    entry_points="""
        [console_scripts]
        sce=sce.cli:cli
    """,
)
