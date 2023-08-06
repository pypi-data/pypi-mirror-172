from setuptools import setup, find_packages

VERSION = "1.0.0"
DESCRIPTION = "Python Packet Übung"

setup(
    name = "projekt_bla_stefan",
    version=VERSION,
    author="Ich halt",
    author_email="emeil@gibds.ned",
    description=DESCRIPTION,
    long_description=open("README").read(),
    long_desscription_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    # Das muß voerher installiert seinn sonst lässt sich das packet nicht installieren
    install_requires= [
        "asyncio",
    ],
    keywords = [
        "python",
        "code",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
)
