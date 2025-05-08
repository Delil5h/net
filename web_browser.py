import sys
import PyQt5.QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class Mainwindow(QMainWindow):
                 def __init__(self):
                         super(Mainwindow,self).__init__()
                         self.showMaximized()
                         self.browser = QwebEngineview()
                         self.browser.setUrl(QUrl('http://localhost:8085'))
                         self.setCentralWidget(self.browser)
                         self.showMaximized()
                         
                         #statusbar
                         statusbar = QToolBar
                         self.addToolBar(statusbar)
                         
                         back_button = QAction('previous',self)
                         back_button.triggered.connection(self.browser.previous)
                         statusbar.addAction(back_button)
                         
                         forward_button = QAction('next',self)
                         forward_button.triggered.connect(self.browser.next)
                         statusbar.addAction(forward_button)
                         
                         refresh_button = QAction('refresh',self)
                         refresh_button.triggered.connect(self.browser.refresh)
                         statusbar.addAction(refresh_button)
                         
                         home_button = QAction('home',self)
                         home_button.triggered.connect(self.nav_home)
                         statusbar.addAction(home_button)
                         
                         
                         self.Url_bar = QLineEdit()
                         self.Url_bar.returnPressed.connect(self.nav_to_url)
                         statusbar.addWidget(self.Url_bar)
                         
                         
                         self.browser.urlChanged.connect(self.update_url)
                         
                         
                         def nav_home(self):
                                self.browser.setUrl(QUrl('http://localhost:8085'))
                          
                         def   nav_to_url(self):
                                      url = self.url_bar.text()
                                      
                                      if not:
                                      url.startswitch('http://') + url
                                      
                                 self.browser.setUrl(QUrl(url))
                                      
                         def    update_url(self,q):
                                 self.url_bar.setText(q.toString())         
                                      
                          
                                      
                
                
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
app = QApplication(sys.argv)
QApplication.setApplicationName('Finder browser')
window = Mainwindow()
app.exec()