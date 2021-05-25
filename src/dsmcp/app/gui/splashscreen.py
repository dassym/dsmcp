'''

:author: F. Voillat
:date: Created on 16 mai 2021
'''
from PyQt5.Qt import QSplashScreen

class AppSplashScreen(QSplashScreen):
    
    def __init__(self, app, pixmap, f):
        self.app = app
        QSplashScreen.__init__(self, pixmap, f)
    
    def drawContents(self, painter):
        QSplashScreen.drawContents(self, painter)
        #painter.setPen(Qt.blue)
        painter.font().setPointSize(30)
        painter.drawText(140,125, self.app.applicationName())
        painter.font().setPointSize(20)
        #painter.drawText(240,125, self.app.appname)
        painter.font().setPointSize(10)
        painter.drawText(140,145, "Version {0:s}".format(*self.app.applicationVersion()))
        
        
