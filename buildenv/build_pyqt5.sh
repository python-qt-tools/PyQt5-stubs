# @Author: Stefan Lehmann
# @Date:   2018-12-06 11:24:07
# @Last Modified by:   Stefan Lehmann
# @Last Modified time: 2019-07-22 13:41:40
VERSION="5.13.0"

wget https://www.riverbankcomputing.com/static/Downloads/PyQt5/$VERSION/PyQt5_gpl-$VERSION.tar.gz -O PyQt5.tar.gz
tar -xvzf PyQt5.tar.gz
cd /root/PyQt5_gpl-$VERSION
python3 configure.py --confirm-license
make
make install
