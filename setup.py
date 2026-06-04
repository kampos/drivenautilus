from setuptools import setup, find_packages

setup(
    name="kadrivesync",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pygobject",
    ],
    entry_points={
        "console_scripts": [
            "kadrivesync=drivenautilus.main:main",
        ],
    },
    package_data={
        "drivenautilus": ["resources/*"],
    },
    data_files=[
        ("share/applications", ["data/org.fonteboa.KADrivesync.desktop"]),
        ("share/metainfo", ["data/org.fonteboa.KADrivesync.metainfo.xml"]),
        ("share/icons/hicolor/scalable/apps", ["data/icons/org.fonteboa.KADrivesync.svg"]),
    ],
)
