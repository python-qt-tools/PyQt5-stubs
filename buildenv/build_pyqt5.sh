# @Author: Stefan Lehmann
# @Date:   2018-12-06 11:24:07
# @Last Modified by:   Stefan Lehmann
# @Last Modified time: 2019-07-23 08:43:52
PYQT_VERSION="5.13.1"
SIP_VERSION="4.19.19"

# build sip
cd /root
wget https://www.riverbankcomputing.com/static/Downloads/sip/$SIP_VERSION/sip-$SIP_VERSION.tar.gz -O sip.tar.gz
tar -xvzf sip.tar.gz
cd sip-*
python3 configure.py --sip-module PyQt5.sip
make
make install
cd /root

# build PyQt5
wget https://www.riverbankcomputing.com/static/Downloads/PyQt5/$PYQT_VERSION/PyQt5_gpl-$PYQT_VERSION.tar.gz -O PyQt5.tar.gz
tar -xvzf PyQt5.tar.gz
cd PyQt5_gpl-$PYQT_VERSION
python3 configure.py --confirm-license
make
make install

# copy stubs
cd /root
mkdir /root/stubs/$PYQT_VERSION
cp /root/PyQt5_gpl-$PYQT_VERSION/*.pyi /root/stubs/$PYQT_VERSION/
