# @Author: Stefan Lehmann
# @Date:   2018-12-06 11:22:17
# @Last Modified by:   Stefan Lehmann
# @Last Modified time: 2019-07-22 13:48:35
VERSION="4.19.18"

wget https://www.riverbankcomputing.com/static/Downloads/sip/$VERSION/sip-$VERSION.tar.gz -O sip.tar.gz
tar -xvzf sip.tar.gz
cd sip-*
python3 configure.py --sip-module PyQt5.sip
make
make install
