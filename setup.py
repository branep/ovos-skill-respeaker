#!/usr/bin/env python3
from setuptools import setup
import os
from os import walk, path


URL = "https://github.com/branep/ovos-skill-respeaker"
SKILL_CLAZZ = "ReSpeaker_4mic_hat"  # needs to match __init__.py class name
PYPI_NAME = "ovos-skill-respeaker"  # pip install PYPI_NAME


# below derived from github url to ensure standard skill_id
SKILL_AUTHOR, SKILL_NAME = URL.split(".com/")[-1].split("/")
SKILL_PKG = SKILL_NAME.lower().replace("-", "_")
PLUGIN_ENTRY_POINT = (
    f"{SKILL_NAME.lower()}.{SKILL_AUTHOR.lower()}={SKILL_PKG}:{SKILL_CLAZZ}"
)
# skill_id=package_name:SkillClass


def find_resource_files():
    # add any folder with files your skill uses here!
    resource_base_dirs = ("locale", "res", "vocab", "dialog", "regex", "skill")
    base_dir = path.dirname(__file__)
    package_data = ["*.json"]
    for res in resource_base_dirs:
        if path.isdir(path.join(base_dir, res)):
            for directory, _, files in walk(path.join(base_dir, res)):
                if files:
                    package_data.append(
                        path.join(directory.replace(base_dir, "").lstrip("/"), "*")
                    )
    return package_data


setup(
    name=PYPI_NAME,
    version="0.1.2",
    url=URL,
    package_dir={SKILL_PKG: ""},
    package_data={SKILL_PKG: find_resource_files()},
    packages=[SKILL_PKG],
    description="Ovos respeaker lights skill",
    author="branep",
    license="Apache-2.0",
    include_package_data=True,
    keywords="ovos skill plugin",
    entry_points={"ovos.plugin.skill": PLUGIN_ENTRY_POINT},
)
