#!/usr/bin/env python3

import unittest

import random

class DiceRoller() :
	def __init__(self, diceSet) :
		self.diceSet = diceSet

	def roll(self) :
		randomFaces = [ dice[random.randint(0,5)] for dice in self.diceSet ]
		random.shuffle(randomFaces)
		return ''.join(randomFaces)

class Game():
	def __init__(self, diceFaces, dictionary) :
		pass

class Boggux_Test(unittest.TestCase) :
	allDifferentDiceSet = [
		'abcçde',
		'fghijk',
		'lmnñop',
		'qrstuv',

		'wxyz01',
		'234567',
		'89ABCÇ',
		'DEFGHI',

		'JKLMNÑ',
		'OPQRST',
		'UVWXYZ',
		'%&#@|*',

		'[](){}',
		':;.,?!',
		'-+=<>/',
		'$€¢Ŧ¥Ł',
		]
	game = (
		'ABCD'
		'FGHI'
		'JKLM'
		'NÑOP'
		)
	def setUp(self) :
		self.gameSetup = None

	def test_diceRoller(self) :
		diceSet = self.allDifferentDiceSet.copy()
		roller = DiceRoller(diceSet)
		game = roller.roll()
		# Each dice appears once and just once
		self.assertEqual( [1]*16,
			[ sum( 1 if face in dice else 0 for dice in diceSet) for face in game ])
		self.assertEqual( [1]*16,
			[ sum( 1 if face in dice else 0 for face in game) for dice in diceSet ])

	def test_goodPath_whenShort(self) :
		self.assertFalse(goodPath([]))
		self.assertFalse(goodPath([1]))
		self.assertFalse(goodPath([1,2]))

	def test_goodPath_whenLongEnough(self) :
		self.assertTrue(goodPath([1,2,3]))

	"""
	00 01 02 03
	04 05 06 07
	08 09 10 11
	12 13 14 15
	"""

	def test_contiguousDices_whenEast(self) :
		self.assertTrue(contiguous(1,2))

	def test_contiguousDices_whenFar(self) :
		self.assertFalse(contiguous(1,3))

	def test_contiguousDices_whenSouth(self) :
		self.assertTrue(contiguous(1,5))

	def test_contiguousDices_whenSouthWest(self) :
		self.assertTrue(contiguous(1,4))

	def test_contiguousDices_whenSouthEast(self) :
		self.assertTrue(contiguous(1,6))

	def test_contiguousDices_whenSouthEast(self) :
		self.assertTrue(contiguous(1,6))

	def test_contiguousDices_whenAtBorderWest(self) :
		self.assertFalse(contiguous(4,7))

	def test_contiguousDices_whenAtBorderEast(self) :
		self.assertFalse(contiguous(3,4))

	def test_contiguousDices_functional_inSide(self) :
		self.assertEqual([
			0,0,0,0,
			0,1,1,1,
			0,1,0,1,
			0,1,1,1,
			],
			[ 1 if contiguous(10,i) else 0  for i in range(16) ])

	def test_contiguousDices_functional_atEdge(self) :
		self.assertEqual([
			0,0,1,1,
			0,0,1,0,
			0,0,1,1,
			0,0,0,0,
			],
			[ 1 if contiguous(7,i) else 0  for i in range(16) ])


	def test_goodPath_whenNotContinuous(self) :
		self.assertFalse(goodPath([1,2,4]))

	def test_goodPath_whenRepeated(self) :
		self.assertFalse(goodPath([1,2,1]))

	def test_wordPath(self) :
		self.assertEqual(
			wordPath(self.game, [1,2,3,6]),
			"BCDH")



def wordPath(game, path) :
	return ''.join(( game[i] for i in path))

def contiguous(first, second) :
	if second < first :
		first, second = second, first
	firstCol = first%4
	step = second-first
	# E and SE if not at E edge
	if step in (1, 5) :
		return firstCol != 3
	# SW if not at W edge
	if step == 3 :
		return firstCol != 0
	# S
	return step == 4

def goodPath(path) :
	# long enough
	if not len(path)>2:
		return False
	# consecutive list
	if not all((contiguous(a,b) for a,b in zip(path,path[1:]))) :
		return False
	# non repeated
	if len(path) != len(set(path)) :
		return False
	return True

from PyQt4 import QtGui
class BogguxDiceBoard(QtGui.QWidget) :
	def __init__(self, parent=None) :
		super(BogguxDiceBoard, self).__init__(parent)


if __name__ == '__main__':
	import sys
	if '--test' in sys.argv:
		sys.argv.remove('--test')
		unittest.main()

	app = QtGui.QApplication(sys.argv)
	w = BogguxDiceBoard()
	w.show()
	app.exec_()


