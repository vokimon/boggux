#!/usr/bin/env python3

import unittest

import random

spanishDiceSet="""
	HERINS
	DAMEPC
	ESFIHE
	UOETNK

	ZVNDAE
	VITEGN
	TAOAEI
	RCALES

	SIRMOA
	GENLUY
	JAMQOB
	WILRUE

	SEONTD
	XORFIA
	BATRIL
	LUSPET
	""".strip().split()


class DiceRoller() :
	def __init__(self, diceSet) :
		self.diceSet = diceSet

	def roll(self) :
		randomFaces = [ dice[random.randint(0,5)] for dice in self.diceSet ]
		random.shuffle(randomFaces)
		return ''.join(randomFaces)

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
		'NOPQ'
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
		self.assertEqual(
			'....'
			'.XXX'
			'.X.X'
			'.XXX'
			, ''.join([ 'X' if contiguous(10,i) else '.'  for i in range(16) ]) )
	def test_contiguousDices_functional_atEdge(self) :
		self.assertEqual(
			'..XX'
			'..X.'
			'..XX'
			'....'
			, ''.join([ 'X' if contiguous(7,i) else '.' for i in range(16) ]))

	def test_prettyPrint(self) :
		g = Game('ABCD''EFGH''IJKL''MNOP')
		self.assertMultiLineEqual(
			'ABCD\n'
			'EFGH\n'
			'IJKL\n'
			'MNOP',
			g.prettyPrint())

	def test_goodPath_whenNotContinuous(self) :
		self.assertFalse(goodPath([1,2,4]))

	def test_goodPath_whenRepeated(self) :
		self.assertFalse(goodPath([1,2,1]))

	def test_wordPath(self) :
		self.assertEqual(
			wordPath(self.game, [1,2,3,6]),
			"BCDH")

	def test_diceReducer_withWordMatching(self):
		d = DiceReducer("abcde")
		self.assertTrue(d.matches("cacadebaca"))

	def test_diceReducer_withWordMatching(self):
		d = DiceReducer("abcde")
		self.assertFalse(d.matches("cacadevaca"))

	def test_diceReducer_withoutEquivalencesAccents(self):
		d = DiceReducer("abcde")
		self.assertFalse(d.matches("cacádèbàçé"))

	def test_diceReducer_withEquivalences(self):
		equivalences={
			'e': 'éè',
			'a': 'àá',
			'c': 'ç'
			}
		d = DiceReducer("abcde", equivalences)
		self.assertTrue(d.matches("cacádèbàçé"))

	def test_reduceWordList(self):
		wordlist = 'casa lata ceta placa jota rota'.split()
		diceList = 'csalpjtozxwy'
		reducer=DiceReducer(diceList)
		self.assertEqual(
			'casa jota lata placa'.split(),
			list(sorted(reducer.reduceWordList(wordlist))))

	def test_reduceWordList_withAccents(self):
		wordlist = 'casà latá ceta placa jota rota'.split()
		diceList = 'csalpjtozxwy'
		reducer = DiceReducer(diceList, equivalences={'a':'àá'})
		self.assertEqual(
			'casà jota latá placa'.split(),
			list(sorted(reducer.reduceWordList(wordlist))))

	def test_reduceWordList_noShortWords(self):
		wordlist = 'ca la ceta placa jota rota'.split()
		diceList = 'csalpjtozxwy'
		reducer = DiceReducer(diceList)
		self.assertEqual(
			'jota placa'.split(),
			list(sorted(reducer.reduceWordList(wordlist))))

	def test_findLetter_withOneOccurrence(self):
		game = Game('AEAA''AAAA''AAAA''AAAA')
		self.assertEqual(game.findLetter('e'), [1])

	def test_findLetter_withNoOccurrences(self):
		game = Game('AAAA''AAAA''AAAA''AAAA')
		self.assertEqual(game.findLetter('e'), [])

	def test_findLetter_withManyOccurrences(self):
		game = Game('AEAA''AAAA''AAAA''AAAE')
		self.assertEqual(game.findLetter('e'), [1,15])

	def test_unaccent_withNormal(self):
		game = Game('AAAA''AAAA''AAAA''AAAA', equivalences={'e':'é'})
		self.assertEqual(game.unaccent('e'),'e')

	def test_unaccent_withEquivalent(self):
		game = Game('AAAA''AAAA''AAAA''AAAA', equivalences={'e':'é'})
		self.assertEqual(game.unaccent('é'),'e')

	def test_findLetter_withAccent_singleEquivalent(self):
		game = Game('AEAA''AAAA''AAAA''AAAE', equivalences={'e':'é'})
		self.assertEqual(game.findLetter('é'), [1,15])

	def test_findNextTrail_whenNoNext(self) :
		game = Game('AAAA''AAAA''AAAA''AAAA')
		self.assertEqual(None,
			game.findNextTrail([5,6],'o'))

	def test_findNextTrail_E(self) :
		game = Game('AAAA''AAAO''AAAA''AAAA')
		self.assertEqual([5,6,7],
			game.findNextTrail([5,6],'o'))

	def test_findNextTrail_NE(self) :
		game = Game('AAAO''AAAA''AAAA''AAAA')
		self.assertEqual([5,6,3],
			game.findNextTrail([5,6],'o'))

	def test_findNextTrail_N(self) :
		game = Game('AAOA''AAAA''AAAA''AAAA')
		self.assertEqual([5,6,2],
			game.findNextTrail([5,6],'o'))

	def test_findNextTrail_NW(self) :
		game = Game('AOAA''AAAA''AAAA''AAAA')
		self.assertEqual([5,6,1],
			game.findNextTrail([5,6],'o'))

	def test_findNextTrail_SW(self) :
		game = Game('AAAA''AAAA''AOAA''AAAA')
		self.assertEqual([5,6,9],
			game.findNextTrail([5,6],'o'))

	def test_findNextTrail_S(self) :
		game = Game('AAAA''AAAA''AAOA''AAAA')
		self.assertEqual([5,6,10],
			game.findNextTrail([5,6],'o'))

	def test_findNextTrail_SE(self) :
		game = Game('AAAA''AAAA''AAAO''AAAA')
		self.assertEqual([5,6,11],
			game.findNextTrail([5,6],'o'))

	def test_findNextTrail_W(self):
		game = Game('AAAA''AOAA''AAAA''AAAA')
		self.assertEqual([2,6,5],
			game.findNextTrail([2,6],'o'))

	def test_findNextTrail_backOnTrail(self):
		game = Game('AAAA''AOAA''AAAA''AAAA')
		self.assertEqual(None,
			game.findNextTrail([5,6],'o'))

	def test_findNextTrail_dontSearchTooNorth(self):
		game = Game('AAAA''AAAA''AAAA''OOOO')
		self.assertEqual(None,
			game.findNextTrail([1],'o'))

	def test_findNextTrail_dontSearchTooSouth(self):
		game = Game('AAAA''AAAA''AAAA''AAAA')
		self.assertEqual(None,
			game.findNextTrail([14],'o'))

	def test_findNextTrail_dontSearchTooEast(self):
		game = Game('AAAA''OAAA''OAAA''OAAA')
		self.assertEqual(None,
			game.findNextTrail([7],'o'))

	def test_findNextTrail_dontSearchTooWest(self):
		game = Game('AAAA''AAAO''AAAO''AAAO')
		self.assertEqual(None,
			game.findNextTrail([4],'o'))

	def test_findNextTrail_noRemaining(self) :
		game = Game('AAAA''AAAA''AAAA''AAAA')
		self.assertEqual([5,6],
			game.findNextTrail([5,6],''))

	def test_findNextTrail_moreLettersRequired(self) :
		game = Game('AAOA''AAAA''AAAA''AAAA')
		self.assertEqual(None,
			game.findNextTrail([5,6],'oi'))

	def test_findNextTrail_moreLettersRequiredAndFound(self) :
		game = Game('AAOI''AAAA''AAAA''AAAA')
		self.assertEqual([5,6,2,3],
			game.findNextTrail([5,6],'oi'))

	def test_findNextTrail_moreLettersRequiredAndFound(self) :
		game = Game('AAOI''AAAA''AAAA''AAAA')
		self.assertEqual([5,6,2,3],
			game.findNextTrail([5,6],'oi'))

class Game() :
	def __init__(self, dices, equivalences={}):
		self.dices = dices.lower()
		self.equivalents = equivalences
		self.reducer = DiceReducer(dices.lower(), equivalences)

	def solve(self, wordlist):
		return [
			word for word in (
				w for w in wordlist if self.reducer.matches(w) )
			if self.hasWord(word)
			]

	def hasWord(self, word):
		if not self.reducer.matches(word): return False
		return self.wordTrail(word) is not None

	def hasWord(self, word):
		return self.wordTrail(word) is not None

	def wordTrail(self, word):
		word = ''.join(self.unaccent(c) for c in word.lower())
		for begin in self.findLetter(word[0]) :
			trail = self.findNextTrail([begin],word[1:])
			if trail: return trail
		return None

	def findNextTrail(self, trail, remaining):
		if not remaining: return trail
		previous = trail[-1]
		for step in -5,-4,-3,-1,+1,+3,+4,+5:
			dice = previous+step
			if dice<0: continue # Too North
			if dice>15: continue # Too South
			previousRow = previous % 4
			diceRow = dice % 4
			if previousRow is 3 and diceRow is 0: continue # Too East
			if previousRow is 0 and diceRow is 3: continue # Too West
			if self.dices[dice] != remaining[0]: continue # Not matching
			if dice in trail: continue # Already in trail
			return self.findNextTrail(trail+[dice], remaining[1:])
		return None

	def findLetter(self,letter):
		letter = self.unaccent(letter)
		return [i for i,c in enumerate(self.dices) if c==letter]

	def prettyPrint(self):
		letters=self.dices.upper()
		return '\n'.join(
			letters[n:n+4]
			for n in range(0,16,4)
			)

	def unaccent(self, letter):
		for unaccent, accented in self.equivalents.items():
			if letter in accented:
				return unaccent
		return letter


class DiceReducer() :
	"""
	Discards words containing letters not included in a dice list.
	This is not resolving the Boggle but quickly reduces the word list
	two factors of magnitude.

	A dicctionary with letter equivalences can be provided to consider,
	for example, a set of tilded caracters equivalent to the untilded one.
	"""
	def __init__(self, diceletters, equivalences={}):
		diceletters+= ''.join([
			equivalences
			for letter, equivalences in equivalences.items()
			if letter in diceletters])
		import re
		self.rege = re.compile('['+''.join(set(diceletters))+']{3,}')

	def matches(self, word):
		return self.rege.fullmatch(word) is not None

	def reduceWordList(self, wordlist) :
		return set([ word for word in wordlist if self.matches(word) ])


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


import time
class benchmark(object):
    def __init__(self,name):
        self.name = name
    def __enter__(self):
        self.start = time.time()
    def __exit__(self,ty,val,tb):
        end = time.time()
        print("%s : %0.3f seconds" % (self.name, end-self.start))
        return False

if __name__ == '__main__':
	import sys
	if '--test' in sys.argv:
		sys.argv.remove('--test')
		unittest.main()

	print('Rolling dices...')
	roller = DiceRoller(spanishDiceSet)
	game = roller.roll()
	game = "BGJZIATEEONUSNSR"
	print(Game(game).prettyPrint())
	print('Prefiltering words...')
	reducer = DiceReducer(game.lower())

	with benchmark("two steps and a half"):
		words = [
			word for word in (
				w.strip() for w in open('wordlist.es.dict'))
		if reducer.matches(word)]

		print(len(Game(game).solve(words)))

	with benchmark("single step"):
		originalWordlist = [w.strip() for w in open('wordlist.es.dict')]
		availableWords = [w for w in Game(game).solve(originalWordlist)]
		print(len(availableWords))

	print("Original word list length: {}".format(len(originalWordlist)))
	print('Reduced to {} words.'.format(len(words)))

	print(availableWords)
	print(len(availableWords))












