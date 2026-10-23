from PyQt5 import sip


if hasattr(sip, 'SIP_ABI_VERSION'):
    abi_version: int = sip.SIP_ABI_VERSION
    assert isinstance(abi_version, int)
