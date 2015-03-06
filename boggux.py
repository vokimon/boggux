#!/usr/bin/env python3
from PyQt5 import QtQuick, QtWidgets, QtCore, QtQml
import sys

if __name__ == '__main__':
	import sys

	app = QtWidgets.QApplication(sys.argv)
	engine = QtQml.QQmlApplicationEngine('boggux.qml')
	w = engine.rootObjects()[0]
	w.show()
	sys.exit(app.exec_())
