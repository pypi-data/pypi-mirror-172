# © Copyright Databand.ai, an IBM Company 2022

import os

import setuptools


BASE_PATH = os.path.dirname(__file__)
CFG_PATH = os.path.join(BASE_PATH, "setup.cfg")

config = setuptools.config.read_configuration(CFG_PATH)
version = config["metadata"]["version"]

setuptools.setup(
    name="dbnd-postgres",
    package_dir={"": "src"},
    install_requires=[
        "psycopg2-binary",
        "pyyaml",
        "pyrsistent<0.15.6",
        "dbnd==" + version,
    ],
    entry_points={},
)
