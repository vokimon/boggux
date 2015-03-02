#!/usr/bin/env python3
from PyQt5 import QtQuick, QtGui, QtCore
import sys

if __name__ == '__main__':
	import sys
	app = QtGui.QGuiApplication(sys.argv)
	w = QtQuick.QQuickView(QtCore.QUrl('boggux.qml'))
	w.show()
	sys.exit(app.exec_())
