from setuptools import setup, find_packages

try:
    from pypandoc import convert
    def read_markdown(file: str) -> str:
        return convert(file, "rst")
except ImportError:
    def read_markdown(file: str) -> str:
        return open(file, "r").read()

setup(
    name="openstackinfo",
    version="5.5.0",
    packages=find_packages(exclude=["tests"]),
    install_requires=open("requirements.txt", "r").readlines(),
    url="https://github.com/wtsi-hgi/openstack-info",
    license="MIT",
    description="Gets information about what is in an OpenStack tenant",
    long_description=read_markdown("README.md"),
    entry_points={
        "console_scripts": [
            "openstackinfo=openstackinfo.entrypoint:main"
        ]
    }
)
