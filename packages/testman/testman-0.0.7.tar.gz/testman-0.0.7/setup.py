import os
import re
import setuptools

NAME             = "testman"
AUTHOR           = "Christophe VG"
AUTHOR_EMAIL     = "contact@christophe.vg"
DESCRIPTION      = "A manager for automated testing by humans"
LICENSE          = "MIT"
KEYWORDS         = "manager testing human"
URL              = "https://github.com/christophevg/" + NAME
README           = ".github/README.md"
CLASSIFIERS      = [
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.8",
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  
]
INSTALL_REQUIRES = [
  "pyyaml",
  "dotmap",
  "fire",
  "python-dotenv",
  "pymongo",
  
]
ENTRY_POINTS = {
  "console_scripts" : [
    "testman=testman.__main__:cli",
    
  ]
}
SCRIPTS = [
  
]

HERE = os.path.dirname(__file__)

def read(file):
  with open(os.path.join(HERE, file), "r") as fh:
    return fh.read()

VERSION = re.search(
  r'__version__ = [\'"]([^\'"]*)[\'"]',
  read(NAME.replace("-", "_") + "/__init__.py")
).group(1)

LONG_DESCRIPTION = read(README)

if __name__ == "__main__":
  setuptools.setup(
    name=NAME,
    version=VERSION,
    packages=setuptools.find_packages(),
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    keywords=KEYWORDS,
    url=URL,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    entry_points=ENTRY_POINTS,
    scripts=SCRIPTS,
    include_package_data=True    
  )
