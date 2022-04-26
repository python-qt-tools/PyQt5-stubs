from PyQt5.QtDataVisualization import QCustom3DVolume
from PyQt5 import sip

v = sip.voidptr(0)
a = v.asarray(1)

volume = QCustom3DVolume()
volume.setTextureData(a)
a = volume.textureData()

# more voidptr tests
v = sip.voidptr(None)
v = sip.voidptr(b'123', 0)
v = sip.voidptr(bytearray(b'123'), 0, False)
v = sip.voidptr(v)
