#!/usr/bin/env python3
from PyQt5 import QtQuick, QtWidgets, QtCore, QtQml
import sys

from bogguxEngine import Game, DiceRoller, spanishDiceSet

class Controller(QtCore.QObject) :
	def __init__(self, parent, window, language):
		super(Controller, self).__init__(parent)
		self.window = window
		self.roller = DiceRoller(spanishDiceSet)
		self.wordlist = [
			word for word in (
				w.strip() for w in open('wordlist.{}.dict'.format(language))
			) if word ]
		self.shuffle()

	@QtCore.pyqtSlot()
	def shuffle(self):
		dices = self.roller.roll()
		self.game = Game(dices)
		self.window.setGame(dices)
		self.validWords = self.game.solve(self.wordlist)
		print(dices)
		print(self.validWords)

	@QtCore.pyqtSlot(str)
	def wordCompleted(self, word):
		message = self.validateWord(word)
		if message:
			return self.window.badWord(word,message)
		points = self.wordPoints(word)
		self.window.goodWord(word,
			self.tr("¡1 punto!") if points==1 else
			self.tr("¡{0} puntos!").format(points))

	def wordPoints(self,word):
		points = len(word)-2
		return points if points>0 else 0

	def validateWord(self,word):
		if len(word)<3:
			return self.tr("Corta")
		if word in self.window.property('words'):
			return self.tr("Repetida")
		if word.lower() not in self.validWords:
			return self.tr("No existe")



if __name__ == '__main__':

	import sys

	lang = sys.argv[1] if len(sys.argv) > 1 else 'es'

	app = QtWidgets.QApplication(sys.argv)
	engine = QtQml.QQmlApplicationEngine()
	engine.load('boggux.qml')
	w = engine.rootObjects()[0]
	context = engine.rootContext()
	context.setContextProperty("gameEngine", Controller(context,w,language=lang));
	w.show()
	sys.exit(app.exec_())

