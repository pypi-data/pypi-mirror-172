from setuptools import setup

with open("README.md", "r") as f:
    page_description = f.read()

setup(
    name="testepypi",
    version="0.0.1",
    author="Argus",
    author_email="argusportal@gmail.com",
    description="My short description",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArgusPortal"
)
