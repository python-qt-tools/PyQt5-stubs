# Careful, the version and build date are both dates, but different formats
ARG ARCH_VERSION="20200407"
ARG BUILD_DATE="2020/04/22"

ARG PYQT_VERSION="5.14.2"
ARG PYQT_3D_VERSION="5.14.0"
ARG PYQT_CHART_VERSION="5.14.0"
ARG PYQT_DATA_VISUALIZATION_VERSION="5.14.0"
ARG PYQT_PURCHASING_VERSION="5.14.0"
ARG PYQT_WEB_ENGINE_VERSION="5.14.0"

################################################################################
# Build dependencies
################################################################################

FROM archlinux:${ARCH_VERSION} AS build-dep

# Reuse argument from previous build scope
ARG BUILD_DATE

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
        # Used to build other PyQt modules in later build stages
        python-pyqt5 \
        # Qt core
        qt5-base  \
        # Qt modules not included in qt5-base
        qt5-3d \
        qt5-charts \
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

################################################################################
# PyQt5 core stubs
################################################################################

FROM build-dep AS pyqt5

# Reuse argument from previous build scope
ARG PYQT_VERSION

# Download source tar
RUN wget --no-verbose \
    --output-document upstream.tar.gz \
    https://pypi.io/packages/source/p/pyqt5/PyQt5-${PYQT_VERSION}.tar.gz
RUN mkdir /upstream/ && \
    tar -xf \
        upstream.tar.gz \
        --directory /upstream/ \
        --strip-components 1

# Build PyQt with stubs
# TODO: Find way to build only stubs. This takes way too long
WORKDIR /upstream/
RUN sip-install \
    --qmake /usr/bin/qmake-qt5 \
    --confirm-license \
    --pep484-pyi \
    --build-dir ./build \
    --verbose

# Copy all .pyi files to output dir
WORKDIR /output/
RUN find /upstream/ -name \*.pyi -exec cp {} . \;

################################################################################
# PyQt3D
################################################################################

FROM build-dep AS pyqt-3d

# Reuse argument from previous build scope
ARG PYQT_3D_VERSION

# Download source tar
RUN wget --no-verbose \
    --output-document upstream.tar.gz \
    https://pypi.io/packages/source/p/pyqt3d/PyQt3D-${PYQT_3D_VERSION}.tar.gz
RUN mkdir /upstream/ && \
    tar -xf \
        upstream.tar.gz \
        --directory /upstream/ \
        --strip-components 1

# Build PyQt3D with stubs
# TODO: Find way to build only stubs
WORKDIR /upstream/
RUN sip-install \
    --qmake /usr/bin/qmake-qt5 \
    --pep484-pyi \
    --build-dir ./build \
    --verbose

# Copy all .pyi files to output dir
WORKDIR /output/
RUN find /upstream/ -name \*.pyi -exec cp {} . \;

################################################################################
# PyQtChart
################################################################################

FROM build-dep AS pyqt-chart

# Reuse argument from previous build scope
ARG PYQT_CHART_VERSION

# Download source tar
RUN wget --no-verbose \
    --output-document upstream.tar.gz \
    https://pypi.io/packages/source/p/pyqtchart/PyQtChart-${PYQT_CHART_VERSION}.tar.gz
RUN mkdir /upstream/ && \
    tar -xf \
        upstream.tar.gz \
        --directory /upstream/ \
        --strip-components 1

# Build PyQtChart with stubs
# TODO: Find way to build only stubs
WORKDIR /upstream/
RUN sip-install \
    --qmake /usr/bin/qmake-qt5 \
    --pep484-pyi \
    --build-dir ./build \
    --verbose

# Copy all .pyi files to output dir
WORKDIR /output/
RUN find /upstream/ -name \*.pyi -exec cp {} . \;

################################################################################
# PyQtDataVisualization
################################################################################

FROM build-dep AS pyqt-data-visualization

# Reuse argument from previous build scope
ARG PYQT_DATA_VISUALIZATION_VERSION

# Download source tar
RUN wget --no-verbose \
    --output-document upstream.tar.gz \
    https://pypi.io/packages/source/p/pyqtdatavisualization/PyQtDataVisualization-${PYQT_DATA_VISUALIZATION_VERSION}.tar.gz
RUN mkdir /upstream/ && \
    tar -xf \
        upstream.tar.gz \
        --directory /upstream/ \
        --strip-components 1

# Build PyQtDataVisualization with stubs
# TODO: Find way to build only stubs
WORKDIR /upstream/
RUN sip-install \
    --qmake /usr/bin/qmake-qt5 \
    --pep484-pyi \
    --build-dir ./build \
    --verbose

# Copy all .pyi files to output dir
WORKDIR /output/
RUN find /upstream/ -name \*.pyi -exec cp {} . \;

################################################################################
# PyQtPurchasing
################################################################################

FROM build-dep AS pyqt-purchasing

# Reuse argument from previous build scope
ARG PYQT_PURCHASING_VERSION

# Download source tar
RUN wget --no-verbose \
    --output-document upstream.tar.gz \
    https://pypi.io/packages/source/p/pyqtpurchasing/PyQtPurchasing-${PYQT_PURCHASING_VERSION}.tar.gz
RUN mkdir /upstream/ && \
    tar -xf \
        upstream.tar.gz \
        --directory /upstream/ \
        --strip-components 1

# Build PyQtPurchasing with stubs
# TODO: Find way to build only stubs
WORKDIR /upstream/
RUN sip-install \
    --qmake /usr/bin/qmake-qt5 \
    --pep484-pyi \
    --build-dir ./build \
    --verbose

# Copy all .pyi files to output dir
WORKDIR /output/
RUN find /upstream/ -name \*.pyi -exec cp {} . \;

################################################################################
# PyQtWebEngine
################################################################################

FROM build-dep AS pyqt-web-engine

# Reuse argument from previous build scope
ARG PYQT_WEB_ENGINE_VERSION

# Download source tar
RUN wget --no-verbose \
    --output-document upstream.tar.gz \
    https://pypi.io/packages/source/p/pyqtwebengine/PyQtWebEngine-${PYQT_WEB_ENGINE_VERSION}.tar.gz
RUN mkdir /upstream/ && \
    tar -xf \
        upstream.tar.gz \
        --directory /upstream/ \
        --strip-components 1

# Build PyQtWebEngine with stubs
# TODO: Find way to build only stubs
WORKDIR /upstream/
RUN sip-install \
    --qmake /usr/bin/qmake-qt5 \
    --pep484-pyi \
    --build-dir ./build \
    --verbose

# Copy all .pyi files to output dir
WORKDIR /output/
RUN find /upstream/ -name \*.pyi -exec cp {} . \;

################################################################################
# Output
################################################################################

FROM scratch AS output

# Get all the outputs from the build layers
WORKDIR /output/
COPY --from=pyqt5 /output/* ./
COPY --from=pyqt-3d /output/* ./
COPY --from=pyqt-chart /output/* ./
COPY --from=pyqt-data-visualization /output/* ./
COPY --from=pyqt-purchasing /output/* ./
COPY --from=pyqt-web-engine /output/* ./

# Required to run the image (which we need to do to get the files)
CMD /bin/true
