# @Author: Stefan Lehmann
# @Date:   2018-12-06 11:22:17
# @Last Modified by:   Stefan Lehmann
# @Last Modified time: 2018-12-06 16:12:24
wget https://sourceforge.net/projects/pyqt/files/sip/sip-4.19.13/sip-4.19.13.tar.gz -O sip.tar.gz
tar -xvzf sip.tar.gz
cd sip-*
python3 configure.py --sip-module PyQt5.sip --no-tools
make
make install
