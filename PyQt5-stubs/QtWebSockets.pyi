# The PEP 484 type hints stub file for the QtWebSockets module.
#
# Generated by SIP 6.0.2
#
# Copyright (c) 2021 Riverbank Computing Limited <info@riverbankcomputing.com>
# 
# This file is part of PyQt5.
# 
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
# 
# If you do not wish to use this file under the terms of the GPL version 3.0
# then you may purchase a commercial license.  For more information contact
# info@riverbankcomputing.com.
# 
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.


import typing

from PyQt5 import sip
from PyQt5 import QtNetwork
from PyQt5 import QtCore

# Support for QDate, QDateTime and QTime.
import datetime

# Convenient type aliases.
PYQT_SLOT = typing.Union[typing.Callable[..., None], QtCore.pyqtBoundSignal]


class QMaskGenerator(QtCore.QObject):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def nextMask(self) -> int: ...
    def seed(self) -> bool: ...


class QWebSocket(QtCore.QObject):

    def __init__(self, origin: str = ..., version: 'QWebSocketProtocol.Version' = ..., parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    @staticmethod
    def maxOutgoingFrameSize() -> int: ...
    def outgoingFrameSize(self) -> int: ...
    def setOutgoingFrameSize(self, outgoingFrameSize: int) -> None: ...
    @staticmethod
    def maxIncomingFrameSize() -> int: ...
    @staticmethod
    def maxIncomingMessageSize() -> int: ...
    def maxAllowedIncomingMessageSize(self) -> int: ...
    def setMaxAllowedIncomingMessageSize(self, maxAllowedIncomingMessageSize: int) -> None: ...
    def maxAllowedIncomingFrameSize(self) -> int: ...
    def setMaxAllowedIncomingFrameSize(self, maxAllowedIncomingFrameSize: int) -> None: ...
    def bytesToWrite(self) -> int: ...
    def preSharedKeyAuthenticationRequired(self, authenticator: QtNetwork.QSslPreSharedKeyAuthenticator) -> None: ...
    def sslErrors(self, errors: typing.Iterable[QtNetwork.QSslError]) -> None: ...
    def bytesWritten(self, bytes: int) -> None: ...
    def pong(self, elapsedTime: int, payload: typing.Union[QtCore.QByteArray, bytes, bytearray]) -> None: ...
    def binaryMessageReceived(self, message: typing.Union[QtCore.QByteArray, bytes, bytearray]) -> None: ...
    def textMessageReceived(self, message: str) -> None: ...
    def binaryFrameReceived(self, frame: typing.Union[QtCore.QByteArray, bytes, bytearray], isLastFrame: bool) -> None: ...
    def textFrameReceived(self, frame: str, isLastFrame: bool) -> None: ...
    def readChannelFinished(self) -> None: ...
    def proxyAuthenticationRequired(self, proxy: QtNetwork.QNetworkProxy, pAuthenticator: QtNetwork.QAuthenticator) -> None: ...
    def stateChanged(self, state: QtNetwork.QAbstractSocket.SocketState) -> None: ...
    def disconnected(self) -> None: ...
    def connected(self) -> None: ...
    def aboutToClose(self) -> None: ...
    def ping(self, payload: typing.Union[QtCore.QByteArray, bytes, bytearray] = ...) -> None: ...
    @typing.overload
    def open(self, url: QtCore.QUrl) -> None: ...
    @typing.overload
    def open(self, request: QtNetwork.QNetworkRequest) -> None: ...
    def close(self, closeCode: 'QWebSocketProtocol.CloseCode' = ..., reason: str = ...) -> None: ...
    def request(self) -> QtNetwork.QNetworkRequest: ...
    def sslConfiguration(self) -> QtNetwork.QSslConfiguration: ...
    def setSslConfiguration(self, sslConfiguration: QtNetwork.QSslConfiguration) -> None: ...
    @typing.overload
    def ignoreSslErrors(self, errors: typing.Iterable[QtNetwork.QSslError]) -> None: ...
    @typing.overload
    def ignoreSslErrors(self) -> None: ...
    def sendBinaryMessage(self, data: typing.Union[QtCore.QByteArray, bytes, bytearray]) -> int: ...
    def sendTextMessage(self, message: str) -> int: ...
    def closeReason(self) -> str: ...
    def closeCode(self) -> 'QWebSocketProtocol.CloseCode': ...
    def origin(self) -> str: ...
    def requestUrl(self) -> QtCore.QUrl: ...
    def resourceName(self) -> str: ...
    def version(self) -> 'QWebSocketProtocol.Version': ...
    def state(self) -> QtNetwork.QAbstractSocket.SocketState: ...
    def setPauseMode(self, pauseMode: typing.Union[QtNetwork.QAbstractSocket.PauseModes, QtNetwork.QAbstractSocket.PauseMode]) -> None: ...
    def resume(self) -> None: ...
    def setReadBufferSize(self, size: int) -> None: ...
    def readBufferSize(self) -> int: ...
    def maskGenerator(self) -> QMaskGenerator: ...
    def setMaskGenerator(self, maskGenerator: QMaskGenerator) -> None: ...
    def setProxy(self, networkProxy: QtNetwork.QNetworkProxy) -> None: ...
    def proxy(self) -> QtNetwork.QNetworkProxy: ...
    def peerPort(self) -> int: ...
    def peerName(self) -> str: ...
    def peerAddress(self) -> QtNetwork.QHostAddress: ...
    def pauseMode(self) -> QtNetwork.QAbstractSocket.PauseModes: ...
    def localPort(self) -> int: ...
    def localAddress(self) -> QtNetwork.QHostAddress: ...
    def isValid(self) -> bool: ...
    def flush(self) -> bool: ...
    def errorString(self) -> str: ...
    @typing.overload
    def error(self) -> QtNetwork.QAbstractSocket.SocketError: ...
    @typing.overload
    def error(self, error: QtNetwork.QAbstractSocket.SocketError) -> None: ...
    def abort(self) -> None: ...


class QWebSocketCorsAuthenticator(sip.simplewrapper):

    @typing.overload
    def __init__(self, origin: str) -> None: ...
    @typing.overload
    def __init__(self, other: 'QWebSocketCorsAuthenticator') -> None: ...

    def allowed(self) -> bool: ...
    def setAllowed(self, allowed: bool) -> None: ...
    def origin(self) -> str: ...
    def swap(self, other: 'QWebSocketCorsAuthenticator') -> None: ...


class QWebSocketProtocol(sip.simplewrapper):

    class CloseCode(int):
        CloseCodeNormal = ... # type: QWebSocketProtocol.CloseCode
        CloseCodeGoingAway = ... # type: QWebSocketProtocol.CloseCode
        CloseCodeProtocolError = ... # type: QWebSocketProtocol.CloseCode
        CloseCodeDatatypeNotSupported = ... # type: QWebSocketProtocol.CloseCode
        CloseCodeReserved1004 = ... # type: QWebSocketProtocol.CloseCode
        CloseCodeMissingStatusCode = ... # type: QWebSocketProtocol.CloseCode
        CloseCodeAbnormalDisconnection = ... # type: QWebSocketProtocol.CloseCode
        CloseCodeWrongDatatype = ... # type: QWebSocketProtocol.CloseCode
        CloseCodePolicyViolated = ... # type: QWebSocketProtocol.CloseCode
        CloseCodeTooMuchData = ... # type: QWebSocketProtocol.CloseCode
        CloseCodeMissingExtension = ... # type: QWebSocketProtocol.CloseCode
        CloseCodeBadOperation = ... # type: QWebSocketProtocol.CloseCode
        CloseCodeTlsHandshakeFailed = ... # type: QWebSocketProtocol.CloseCode

    CloseCodeNormal = ...  # type: QWebSocketProtocol.CloseCode
    CloseCodeGoingAway = ...  # type: QWebSocketProtocol.CloseCode
    CloseCodeProtocolError = ...  # type: QWebSocketProtocol.CloseCode
    CloseCodeDatatypeNotSupported = ...  # type: QWebSocketProtocol.CloseCode
    CloseCodeReserved1004 = ...  # type: QWebSocketProtocol.CloseCode
    CloseCodeMissingStatusCode = ...  # type: QWebSocketProtocol.CloseCode
    CloseCodeAbnormalDisconnection = ...  # type: QWebSocketProtocol.CloseCode
    CloseCodeWrongDatatype = ...  # type: QWebSocketProtocol.CloseCode
    CloseCodePolicyViolated = ...  # type: QWebSocketProtocol.CloseCode
    CloseCodeTooMuchData = ...  # type: QWebSocketProtocol.CloseCode
    CloseCodeMissingExtension = ...  # type: QWebSocketProtocol.CloseCode
    CloseCodeBadOperation = ...  # type: QWebSocketProtocol.CloseCode
    CloseCodeTlsHandshakeFailed = ...  # type: QWebSocketProtocol.CloseCode

    class Version(int):
        VersionUnknown = ... # type: QWebSocketProtocol.Version
        Version0 = ... # type: QWebSocketProtocol.Version
        Version4 = ... # type: QWebSocketProtocol.Version
        Version5 = ... # type: QWebSocketProtocol.Version
        Version6 = ... # type: QWebSocketProtocol.Version
        Version7 = ... # type: QWebSocketProtocol.Version
        Version8 = ... # type: QWebSocketProtocol.Version
        Version13 = ... # type: QWebSocketProtocol.Version
        VersionLatest = ... # type: QWebSocketProtocol.Version

    VersionUnknown = ... # type: QWebSocketProtocol.Version
    Version0 = ... # type: QWebSocketProtocol.Version
    Version4 = ... # type: QWebSocketProtocol.Version
    Version5 = ... # type: QWebSocketProtocol.Version
    Version6 = ... # type: QWebSocketProtocol.Version
    Version7 = ... # type: QWebSocketProtocol.Version
    Version8 = ... # type: QWebSocketProtocol.Version
    Version13 = ... # type: QWebSocketProtocol.Version
    VersionLatest = ... # type: QWebSocketProtocol.Version


class QWebSocketServer(QtCore.QObject):

    class SslMode(int):
        SecureMode = ... # type: QWebSocketServer.SslMode
        NonSecureMode = ... # type: QWebSocketServer.SslMode

    SecureMode = ...  # type: QWebSocketServer.SslMode
    NonSecureMode = ...  # type: QWebSocketServer.SslMode

    def __init__(self, serverName: str, secureMode: 'QWebSocketServer.SslMode', parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def handshakeTimeoutMS(self) -> int: ...
    def setHandshakeTimeout(self, msec: int) -> None: ...
    def nativeDescriptor(self) -> sip.voidptr: ...
    def setNativeDescriptor(self, descriptor: sip.voidptr) -> bool: ...
    def preSharedKeyAuthenticationRequired(self, authenticator: QtNetwork.QSslPreSharedKeyAuthenticator) -> None: ...
    def closed(self) -> None: ...
    def sslErrors(self, errors: typing.Iterable[QtNetwork.QSslError]) -> None: ...
    def peerVerifyError(self, error: QtNetwork.QSslError) -> None: ...
    def newConnection(self) -> None: ...
    def originAuthenticationRequired(self, pAuthenticator: QWebSocketCorsAuthenticator) -> None: ...
    def serverError(self, closeCode: QWebSocketProtocol.CloseCode) -> None: ...
    def acceptError(self, socketError: QtNetwork.QAbstractSocket.SocketError) -> None: ...
    def handleConnection(self, socket: QtNetwork.QTcpSocket) -> None: ...
    def serverUrl(self) -> QtCore.QUrl: ...
    def supportedVersions(self) -> typing.List[QWebSocketProtocol.Version]: ...
    def sslConfiguration(self) -> QtNetwork.QSslConfiguration: ...
    def setSslConfiguration(self, sslConfiguration: QtNetwork.QSslConfiguration) -> None: ...
    def proxy(self) -> QtNetwork.QNetworkProxy: ...
    def setProxy(self, networkProxy: QtNetwork.QNetworkProxy) -> None: ...
    def serverName(self) -> str: ...
    def setServerName(self, serverName: str) -> None: ...
    def resumeAccepting(self) -> None: ...
    def pauseAccepting(self) -> None: ...
    def errorString(self) -> str: ...
    def error(self) -> QWebSocketProtocol.CloseCode: ...
    def nextPendingConnection(self) -> QWebSocket: ...
    def hasPendingConnections(self) -> bool: ...
    def socketDescriptor(self) -> int: ...
    def setSocketDescriptor(self, socketDescriptor: int) -> bool: ...
    def secureMode(self) -> 'QWebSocketServer.SslMode': ...
    def serverAddress(self) -> QtNetwork.QHostAddress: ...
    def serverPort(self) -> int: ...
    def maxPendingConnections(self) -> int: ...
    def setMaxPendingConnections(self, numConnections: int) -> None: ...
    def isListening(self) -> bool: ...
    def close(self) -> None: ...
    def listen(self, address: typing.Union[QtNetwork.QHostAddress, QtNetwork.QHostAddress.SpecialAddress] = ..., port: int = ...) -> bool: ...
