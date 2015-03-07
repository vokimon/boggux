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
			game.findNextTrail([1,2],'o'))


class Game() :
	def __init__(self, dices, equivalences={}):
		self.dices = dices.lower()
		self.equivalents = equivalences

	def findNextTrail(self, trail, remaining):
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
		self.rege = re.compile('['+''.join(set(diceletters))+']*')

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


if __name__ == '__main__':
	import sys
	if '--test' in sys.argv:
		sys.argv.remove('--test')
		unittest.main()

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

	print('Rolling dices...')
	roller = DiceRoller(spanishDiceSet)
	game = roller.roll()
	game = "BGJZIATEEONUSNSR"
	print(Game(game).prettyPrint())
	print('Prefiltering words...')
	reducer = DiceReducer(game.lower())
	words = set(
		word for word in (
			w.strip() for w in open('wordlist.es.dict'))
		if reducer.matches(word))
	print('Reduced to {} words.'.format(len(words)))
	print('Testing for a word...')
	for word in [
		'case',
		'date',
		'sar',
		'ret',
		'rets',
		'ree',
		'rees',
		]:
		print(word, (word in words))

	def occurrences(item, alist) :
		i = 0
		while True:
			try:
				i = alist.index(item,i)
			except ValueError:
				raise StopIteration
			yield i
			i+=1
				

	print([i for i in occurrences('E',game)])

	def findTrail(dices, trail, remaining) :
		if not remaining: return trail
		previous = trail[-1]
		for i in -3,-4,-5,-1,+1,+3,+4,+5 :
			step = previous+i
			if step<0: continue
			if step>=16: continue
			if step in trail: continue
			if not contiguous(previous, step): continue
			if remaining[0]!=dices[step]: continue
			found = findTrail(dices, trail+[step],remaining[1:])
			if found: return found

	def wordInGame(game, word) :
		for i in occurrences(word[0],game.lower()) :
			trail = findTrail(game.lower(), [i],word[1:])
			if trail: return trail

	availableWords = [
		word for word in (words)
		if len(word)>2
		and wordInGame(game, word)
		]
	print(availableWords)
	print(len(availableWords))












