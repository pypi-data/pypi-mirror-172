from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

REPO_NAME = "myIPYNBrenderer"
AUTHOR_NAME = "Sumegh20" 
AUTHOR_EMAIL = "sumegh20@gmail.com"

setup(
    name = REPO_NAME,
    version = "0.0.3",
    author = AUTHOR_NAME,
    author_email = AUTHOR_EMAIL,
    description = "A small python package",
    long_description = LONG_DESCRIPTION,
    url = f"https://github.com/{AUTHOR_NAME}/{REPO_NAME}",
    project_urls = {
        "Bug Tracker": f"https://github.com/{AUTHOR_NAME}/{REPO_NAME}/issues"
    },
    package_dir = {"": "src"},
    packages = find_packages(where="src")
)
