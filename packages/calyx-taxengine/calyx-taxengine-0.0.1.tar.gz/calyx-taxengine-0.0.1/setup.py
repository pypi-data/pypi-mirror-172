from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Tax Engine shered module'
LONG_DESCRIPTION = 'Tax Engine shered module'

# Setting up
setup(
    name="calyx-taxengine",
    version=VERSION,
    author="Calyx Servicios",
    author_email="<dev@calyxservicios.com.ar>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['sqlalchemy'],
    keywords=['calyx-servicios', 'tax-engine'],
    classifiers=[]
)