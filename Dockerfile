# Careful, the version and build date are both dates, but different formats
ARG ARCH_VERSION="20200407"
ARG BUILD_DATE="2020/04/22"
ARG PYQT_VERSION="5.14.2"

FROM archlinux:${ARCH_VERSION}

# Reuse arguments from previous build scope
ARG BUILD_DATE
ARG PYQT_VERSION

# Use Arch archive to freeze packages to a certain date
RUN echo "Server=https://archive.archlinux.org/repos/${BUILD_DATE}/\$repo/os/\$arch" \
        | tee /etc/pacman.d/mirrorlist && \
    pacman -Syyuu --noconfirm

# Install build dependencies and Qt Modules
RUN pacman --noconfirm -S \
        # Build stuff
        base-devel wget \
        # PyQt stuff
        pyqt-builder python-sip sip5 \
        # Qt core
        qt5-base  \
        # Qt modules not included in qt5-base
        qt5-3d \
        qt5-connectivity \
        qt5-datavis3d \
        qt5-declarative \
        qt5-gamepad \
        qt5-graphicaleffects \
        qt5-imageformats \
        qt5-location \
        qt5-multimedia \
        qt5-purchasing \
        qt5-networkauth \
        qt5-remoteobjects \
        qt5-script \
        qt5-sensors \
        qt5-serialport \
        qt5-svg \
        qt5-tools \
        qt5-wayland \
        qt5-webchannel \
        qt5-webengine \
        qt5-webkit  \
        qt5-websockets \
        qt5-x11extras \
        qt5-xmlpatterns \
        # Required for QtDBus
        python-dbus

# Download source tar
WORKDIR /upstream/
RUN wget --no-verbose https://pypi.io/packages/source/p/pyqt5/PyQt5-${PYQT_VERSION}.tar.gz
RUN tar -xf PyQt5-${PYQT_VERSION}.tar.gz

# Build PyQt with stubs
# TODO: Find way to build only stubs. This takes way too long
WORKDIR PyQt5-${PYQT_VERSION}/
RUN sip-install \
    --qmake /usr/bin/qmake-qt5 \
    --confirm-license \
    --pep484-pyi \
    --build-dir ./build \
    --verbose

# Copy all .pyi files to output dir
WORKDIR /output/
RUN find /upstream/PyQt5-${PYQT_VERSION}/ -name \*.pyi -exec cp {} . \;
