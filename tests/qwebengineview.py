from PyQt5.QtWebEngineWidgets import QWebEngineView

view = QWebEngineView()
view.setPage(None)

# note: eventhough the page set is None, Qt will create a default page if you
#       retrieve it with page()
