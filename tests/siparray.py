from PyQt5.QtDataVisualization import QCustom3DVolume
from PyQt5 import sip

v = sip.voidptr(0)
a = v.asarray(1)

volume = QCustom3DVolume()
volume.setTextureData(a)
a = volume.textureData()