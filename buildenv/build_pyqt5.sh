# @Author: Stefan Lehmann
# @Date:   2018-12-06 11:24:07
# @Last Modified by:   Stefan Lehmann
# @Last Modified time: 2018-12-06 11:25:36
wget https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.11.3/PyQt5_gpl-5.11.3.tar.gz/download -O PyQt5.tar.gz
tar -xvzf PyQt5.tar.gz
cd /root/PyQt5_gpl-5.11.3
python3 configure.py --confirm-license
make
make install
