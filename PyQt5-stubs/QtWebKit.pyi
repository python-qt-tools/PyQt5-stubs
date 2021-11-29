# The PEP 484 type hints stub file for the QtWebKit module.
#
# Generated by SIP 6.4.0
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

import PyQt5.sip

from PyQt5 import QtNetwork
from PyQt5 import QtGui
from PyQt5 import QtCore

# Support for QDate, QDateTime and QTime.
import datetime

# Convenient type aliases.
PYQT_SIGNAL = typing.Union[QtCore.pyqtSignal, QtCore.pyqtBoundSignal]
PYQT_SLOT = typing.Union[typing.Callable[..., None], QtCore.pyqtBoundSignal]

# Convenient aliases for complicated OpenGL types.
PYQT_OPENGL_ARRAY = typing.Union[typing.Sequence[int], typing.Sequence[float],
        PyQt5.sip.Buffer, None]
PYQT_OPENGL_BOUND_ARRAY = typing.Union[typing.Sequence[int],
        typing.Sequence[float], PyQt5.sip.Buffer, int, None]


class QWebDatabase(sip.simplewrapper):

    def __init__(self, other: 'QWebDatabase') -> None: ...

    @staticmethod
    def removeAllDatabases() -> None: ...
    @staticmethod
    def removeDatabase(db: 'QWebDatabase') -> None: ...
    def origin(self) -> 'QWebSecurityOrigin': ...
    def fileName(self) -> str: ...
    def size(self) -> int: ...
    def expectedSize(self) -> int: ...
    def displayName(self) -> str: ...
    def name(self) -> str: ...


class QWebElement(sip.simplewrapper):

    class StyleResolveStrategy(int):
        InlineStyle = ... # type: QWebElement.StyleResolveStrategy
        CascadedStyle = ... # type: QWebElement.StyleResolveStrategy
        ComputedStyle = ... # type: QWebElement.StyleResolveStrategy

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QWebElement') -> None: ...

    @typing.overload
    def render(self, painter: QtGui.QPainter) -> None: ...
    @typing.overload
    def render(self, painter: QtGui.QPainter, clip: QtCore.QRect) -> None: ...
    def setStyleProperty(self, name: str, value: str) -> None: ...
    def styleProperty(self, name: str, strategy: 'QWebElement.StyleResolveStrategy') -> str: ...
    def evaluateJavaScript(self, scriptSource: str) -> typing.Any: ...
    def removeAllChildren(self) -> None: ...
    def removeFromDocument(self) -> None: ...
    def takeFromDocument(self) -> 'QWebElement': ...
    def clone(self) -> 'QWebElement': ...
    @typing.overload
    def replace(self, markup: str) -> None: ...
    @typing.overload
    def replace(self, element: 'QWebElement') -> None: ...
    @typing.overload
    def encloseWith(self, markup: str) -> None: ...
    @typing.overload
    def encloseWith(self, element: 'QWebElement') -> None: ...
    @typing.overload
    def encloseContentsWith(self, element: 'QWebElement') -> None: ...
    @typing.overload
    def encloseContentsWith(self, markup: str) -> None: ...
    @typing.overload
    def prependOutside(self, markup: str) -> None: ...
    @typing.overload
    def prependOutside(self, element: 'QWebElement') -> None: ...
    @typing.overload
    def appendOutside(self, markup: str) -> None: ...
    @typing.overload
    def appendOutside(self, element: 'QWebElement') -> None: ...
    @typing.overload
    def prependInside(self, markup: str) -> None: ...
    @typing.overload
    def prependInside(self, element: 'QWebElement') -> None: ...
    @typing.overload
    def appendInside(self, markup: str) -> None: ...
    @typing.overload
    def appendInside(self, element: 'QWebElement') -> None: ...
    def webFrame(self) -> QWebFrame: ...
    def document(self) -> 'QWebElement': ...
    def previousSibling(self) -> 'QWebElement': ...
    def nextSibling(self) -> 'QWebElement': ...
    def lastChild(self) -> 'QWebElement': ...
    def firstChild(self) -> 'QWebElement': ...
    def parent(self) -> 'QWebElement': ...
    def namespaceUri(self) -> str: ...
    def localName(self) -> str: ...
    def prefix(self) -> str: ...
    def tagName(self) -> str: ...
    def geometry(self) -> QtCore.QRect: ...
    def setFocus(self) -> None: ...
    def hasFocus(self) -> bool: ...
    def toggleClass(self, name: str) -> None: ...
    def removeClass(self, name: str) -> None: ...
    def addClass(self, name: str) -> None: ...
    def hasClass(self, name: str) -> bool: ...
    def classes(self) -> typing.List[str]: ...
    def attributeNames(self, namespaceUri: str = ...) -> typing.List[str]: ...
    def hasAttributes(self) -> bool: ...
    def removeAttributeNS(self, namespaceUri: str, name: str) -> None: ...
    def removeAttribute(self, name: str) -> None: ...
    def hasAttributeNS(self, namespaceUri: str, name: str) -> bool: ...
    def hasAttribute(self, name: str) -> bool: ...
    def attributeNS(self, namespaceUri: str, name: str, defaultValue: str = ...) -> str: ...
    def attribute(self, name: str, defaultValue: str = ...) -> str: ...
    def setAttributeNS(self, namespaceUri: str, name: str, value: str) -> None: ...
    def setAttribute(self, name: str, value: str) -> None: ...
    def toInnerXml(self) -> str: ...
    def setInnerXml(self, markup: str) -> None: ...
    def toOuterXml(self) -> str: ...
    def setOuterXml(self, markup: str) -> None: ...
    def toPlainText(self) -> str: ...
    def setPlainText(self, text: str) -> None: ...
    def findFirst(self, selectorQuery: str) -> 'QWebElement': ...
    def findAll(self, selectorQuery: str) -> 'QWebElementCollection': ...
    def isNull(self) -> bool: ...


class QWebElementCollection(sip.simplewrapper):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, contextElement: QWebElement, query: str) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QWebElementCollection') -> None: ...

    def toList(self) -> typing.List[QWebElement]: ...
    def last(self) -> QWebElement: ...
    def first(self) -> QWebElement: ...
    def __getitem__(self, i: int) -> QWebElement: ...
    def at(self, i: int) -> QWebElement: ...
    def __len__(self) -> int: ...
    def count(self) -> int: ...
    def append(self, collection: 'QWebElementCollection') -> None: ...


class QWebHistoryItem(sip.simplewrapper):

    def __init__(self, other: 'QWebHistoryItem') -> None: ...

    def isValid(self) -> bool: ...
    def setUserData(self, userData: typing.Any) -> None: ...
    def userData(self) -> typing.Any: ...
    def icon(self) -> QtGui.QIcon: ...
    def lastVisited(self) -> QtCore.QDateTime: ...
    def title(self) -> str: ...
    def url(self) -> QtCore.QUrl: ...
    def originalUrl(self) -> QtCore.QUrl: ...


class QWebHistory(sip.simplewrapper):

    def setMaximumItemCount(self, count: int) -> None: ...
    def maximumItemCount(self) -> int: ...
    def currentItemIndex(self) -> int: ...
    def __len__(self) -> int: ...
    def count(self) -> int: ...
    def itemAt(self, i: int) -> QWebHistoryItem: ...
    def forwardItem(self) -> QWebHistoryItem: ...
    def currentItem(self) -> QWebHistoryItem: ...
    def backItem(self) -> QWebHistoryItem: ...
    def goToItem(self, item: QWebHistoryItem) -> None: ...
    def forward(self) -> None: ...
    def back(self) -> None: ...
    def canGoForward(self) -> bool: ...
    def canGoBack(self) -> bool: ...
    def forwardItems(self, maxItems: int) -> typing.List[QWebHistoryItem]: ...
    def backItems(self, maxItems: int) -> typing.List[QWebHistoryItem]: ...
    def items(self) -> typing.List[QWebHistoryItem]: ...
    def clear(self) -> None: ...


class QWebHistoryInterface(QtCore.QObject):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def addHistoryEntry(self, url: str) -> None: ...
    def historyContains(self, url: str) -> bool: ...
    @staticmethod
    def defaultInterface() -> 'QWebHistoryInterface': ...
    @staticmethod
    def setDefaultInterface(defaultInterface: 'QWebHistoryInterface') -> None: ...


class QWebPluginFactory(QtCore.QObject):

    class Extension(int):

    class MimeType(sip.simplewrapper):

        description = ... # type: str
        fileExtensions = ... # type: typing.Iterable[str]
        name = ... # type: str

        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, a0: 'QWebPluginFactory.MimeType') -> None: ...

    class Plugin(sip.simplewrapper):

        description = ... # type: str
        mimeTypes = ... # type: typing.Iterable['QWebPluginFactory.MimeType']
        name = ... # type: str

        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, a0: 'QWebPluginFactory.Plugin') -> None: ...

    class ExtensionOption(sip.simplewrapper):

        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, a0: 'QWebPluginFactory.ExtensionOption') -> None: ...

    class ExtensionReturn(sip.simplewrapper):

        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, a0: 'QWebPluginFactory.ExtensionReturn') -> None: ...

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def supportsExtension(self, extension: 'QWebPluginFactory.Extension') -> bool: ...
    def extension(self, extension: 'QWebPluginFactory.Extension', option: typing.Optional['QWebPluginFactory.ExtensionOption'] = ..., output: typing.Optional['QWebPluginFactory.ExtensionReturn'] = ...) -> bool: ...
    def create(self, mimeType: str, url: QtCore.QUrl, argumentNames: typing.Iterable[str], argumentValues: typing.Iterable[str]) -> QtCore.QObject: ...
    def refreshPlugins(self) -> None: ...
    def plugins(self) -> typing.List['QWebPluginFactory.Plugin']: ...


class QWebSecurityOrigin(sip.simplewrapper):

    class SubdomainSetting(int):
        AllowSubdomains = ... # type: QWebSecurityOrigin.SubdomainSetting
        DisallowSubdomains = ... # type: QWebSecurityOrigin.SubdomainSetting

    @typing.overload
    def __init__(self, url: QtCore.QUrl) -> None: ...
    @typing.overload
    def __init__(self, other: 'QWebSecurityOrigin') -> None: ...

    def removeAccessWhitelistEntry(self, scheme: str, host: str, subdomainSetting: 'QWebSecurityOrigin.SubdomainSetting') -> None: ...
    def addAccessWhitelistEntry(self, scheme: str, host: str, subdomainSetting: 'QWebSecurityOrigin.SubdomainSetting') -> None: ...
    def setApplicationCacheQuota(self, quota: int) -> None: ...
    @staticmethod
    def localSchemes() -> typing.List[str]: ...
    @staticmethod
    def removeLocalScheme(scheme: str) -> None: ...
    @staticmethod
    def addLocalScheme(scheme: str) -> None: ...
    def databases(self) -> typing.List[QWebDatabase]: ...
    def setDatabaseQuota(self, quota: int) -> None: ...
    def databaseQuota(self) -> int: ...
    def databaseUsage(self) -> int: ...
    def port(self) -> int: ...
    def host(self) -> str: ...
    def scheme(self) -> str: ...
    @staticmethod
    def allOrigins() -> typing.List['QWebSecurityOrigin']: ...


class QWebSettings(sip.simplewrapper):

    class ThirdPartyCookiePolicy(int):
        AlwaysAllowThirdPartyCookies = ... # type: QWebSettings.ThirdPartyCookiePolicy
        AlwaysBlockThirdPartyCookies = ... # type: QWebSettings.ThirdPartyCookiePolicy
        AllowThirdPartyWithExistingCookies = ... # type: QWebSettings.ThirdPartyCookiePolicy

    class FontSize(int):
        MinimumFontSize = ... # type: QWebSettings.FontSize
        MinimumLogicalFontSize = ... # type: QWebSettings.FontSize
        DefaultFontSize = ... # type: QWebSettings.FontSize
        DefaultFixedFontSize = ... # type: QWebSettings.FontSize

    class WebGraphic(int):
        MissingImageGraphic = ... # type: QWebSettings.WebGraphic
        MissingPluginGraphic = ... # type: QWebSettings.WebGraphic
        DefaultFrameIconGraphic = ... # type: QWebSettings.WebGraphic
        TextAreaSizeGripCornerGraphic = ... # type: QWebSettings.WebGraphic
        InputSpeechButtonGraphic = ... # type: QWebSettings.WebGraphic
        SearchCancelButtonGraphic = ... # type: QWebSettings.WebGraphic
        SearchCancelButtonPressedGraphic = ... # type: QWebSettings.WebGraphic

    class WebAttribute(int):
        AutoLoadImages = ... # type: QWebSettings.WebAttribute
        JavascriptEnabled = ... # type: QWebSettings.WebAttribute
        JavaEnabled = ... # type: QWebSettings.WebAttribute
        PluginsEnabled = ... # type: QWebSettings.WebAttribute
        PrivateBrowsingEnabled = ... # type: QWebSettings.WebAttribute
        JavascriptCanOpenWindows = ... # type: QWebSettings.WebAttribute
        JavascriptCanCloseWindows = ... # type: QWebSettings.WebAttribute
        JavascriptCanAccessClipboard = ... # type: QWebSettings.WebAttribute
        DeveloperExtrasEnabled = ... # type: QWebSettings.WebAttribute
        LinksIncludedInFocusChain = ... # type: QWebSettings.WebAttribute
        ZoomTextOnly = ... # type: QWebSettings.WebAttribute
        PrintElementBackgrounds = ... # type: QWebSettings.WebAttribute
        OfflineStorageDatabaseEnabled = ... # type: QWebSettings.WebAttribute
        OfflineWebApplicationCacheEnabled = ... # type: QWebSettings.WebAttribute
        LocalStorageDatabaseEnabled = ... # type: QWebSettings.WebAttribute
        LocalStorageEnabled = ... # type: QWebSettings.WebAttribute
        LocalContentCanAccessRemoteUrls = ... # type: QWebSettings.WebAttribute
        DnsPrefetchEnabled = ... # type: QWebSettings.WebAttribute
        XSSAuditingEnabled = ... # type: QWebSettings.WebAttribute
        AcceleratedCompositingEnabled = ... # type: QWebSettings.WebAttribute
        SpatialNavigationEnabled = ... # type: QWebSettings.WebAttribute
        LocalContentCanAccessFileUrls = ... # type: QWebSettings.WebAttribute
        TiledBackingStoreEnabled = ... # type: QWebSettings.WebAttribute
        FrameFlatteningEnabled = ... # type: QWebSettings.WebAttribute
        SiteSpecificQuirksEnabled = ... # type: QWebSettings.WebAttribute
        WebGLEnabled = ... # type: QWebSettings.WebAttribute
        HyperlinkAuditingEnabled = ... # type: QWebSettings.WebAttribute
        CSSRegionsEnabled = ... # type: QWebSettings.WebAttribute
        CSSGridLayoutEnabled = ... # type: QWebSettings.WebAttribute
        ScrollAnimatorEnabled = ... # type: QWebSettings.WebAttribute
        CaretBrowsingEnabled = ... # type: QWebSettings.WebAttribute
        NotificationsEnabled = ... # type: QWebSettings.WebAttribute
        WebAudioEnabled = ... # type: QWebSettings.WebAttribute
        Accelerated2dCanvasEnabled = ... # type: QWebSettings.WebAttribute

    class FontFamily(int):
        StandardFont = ... # type: QWebSettings.FontFamily
        FixedFont = ... # type: QWebSettings.FontFamily
        SerifFont = ... # type: QWebSettings.FontFamily
        SansSerifFont = ... # type: QWebSettings.FontFamily
        CursiveFont = ... # type: QWebSettings.FontFamily
        FantasyFont = ... # type: QWebSettings.FontFamily

    def cssMediaType(self) -> str: ...
    def setCSSMediaType(self, a0: str) -> None: ...
    def thirdPartyCookiePolicy(self) -> 'QWebSettings.ThirdPartyCookiePolicy': ...
    def setThirdPartyCookiePolicy(self, a0: 'QWebSettings.ThirdPartyCookiePolicy') -> None: ...
    @staticmethod
    def enablePersistentStorage(path: str = ...) -> None: ...
    @staticmethod
    def clearMemoryCaches() -> None: ...
    def localStoragePath(self) -> str: ...
    def setLocalStoragePath(self, path: str) -> None: ...
    @staticmethod
    def offlineWebApplicationCacheQuota() -> int: ...
    @staticmethod
    def setOfflineWebApplicationCacheQuota(maximumSize: int) -> None: ...
    @staticmethod
    def offlineWebApplicationCachePath() -> str: ...
    @staticmethod
    def setOfflineWebApplicationCachePath(path: str) -> None: ...
    def defaultTextEncoding(self) -> str: ...
    def setDefaultTextEncoding(self, encoding: str) -> None: ...
    @staticmethod
    def offlineStorageDefaultQuota() -> int: ...
    @staticmethod
    def setOfflineStorageDefaultQuota(maximumSize: int) -> None: ...
    @staticmethod
    def offlineStoragePath() -> str: ...
    @staticmethod
    def setOfflineStoragePath(path: str) -> None: ...
    @staticmethod
    def setObjectCacheCapacities(cacheMinDeadCapacity: int, cacheMaxDead: int, totalCapacity: int) -> None: ...
    @staticmethod
    def maximumPagesInCache() -> int: ...
    @staticmethod
    def setMaximumPagesInCache(pages: int) -> None: ...
    @staticmethod
    def webGraphic(type: 'QWebSettings.WebGraphic') -> QtGui.QPixmap: ...
    @staticmethod
    def setWebGraphic(type: 'QWebSettings.WebGraphic', graphic: QtGui.QPixmap) -> None: ...
    @staticmethod
    def iconForUrl(url: QtCore.QUrl) -> QtGui.QIcon: ...
    @staticmethod
    def clearIconDatabase() -> None: ...
    @staticmethod
    def iconDatabasePath() -> str: ...
    @staticmethod
    def setIconDatabasePath(location: str) -> None: ...
    def userStyleSheetUrl(self) -> QtCore.QUrl: ...
    def setUserStyleSheetUrl(self, location: QtCore.QUrl) -> None: ...
    def resetAttribute(self, attr: 'QWebSettings.WebAttribute') -> None: ...
    def testAttribute(self, attr: 'QWebSettings.WebAttribute') -> bool: ...
    def setAttribute(self, attr: 'QWebSettings.WebAttribute', on: bool) -> None: ...
    def resetFontSize(self, type: 'QWebSettings.FontSize') -> None: ...
    def fontSize(self, type: 'QWebSettings.FontSize') -> int: ...
    def setFontSize(self, type: 'QWebSettings.FontSize', size: int) -> None: ...
    def resetFontFamily(self, which: 'QWebSettings.FontFamily') -> None: ...
    def fontFamily(self, which: 'QWebSettings.FontFamily') -> str: ...
    def setFontFamily(self, which: 'QWebSettings.FontFamily', family: str) -> None: ...
    @staticmethod
    def globalSettings() -> 'QWebSettings': ...


def qWebKitMinorVersion() -> int: ...
def qWebKitMajorVersion() -> int: ...
def qWebKitVersion() -> str: ...
