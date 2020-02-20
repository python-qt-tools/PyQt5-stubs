# Using the buildenv

The buildenv enables you to create new PyQt5-stubs from scratch.

## Usage

### 1. Update build_pyq5.sh to the latest versions:

Set PYQT5_VERSION and SIP_VERSION according to the current version number on riverbankcomputing.com:

PyQt5: https://www.riverbankcomputing.com/software/pyqt/download5/
SIP: https://www.riverbankcomputing.com/software/sip/download

### 2. Build docker image

Build the image with the following command:

```bash
$ docker build -t pyqt-stubs .
```

### 3. Run the docker image

```bash
$ docker run -it --rm pyqt5-stubs
```

If everything went fine you will find the stub files in the buildenv/stubs directory.

### 4. Create a new branch and replace older modified stub files 

Change to PyQt5-stubs directory and create a branch with the current version
number and *.org* suffix (e.g. 5.13.1.org). Replace the existing stub file with
the freshly created ones.