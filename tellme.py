#!/usr/bin/python

class Board:
	# letters: a string of rxc letters
	# owners: a string of rxc letters
	def __init__(self, letters, owners, r=5, c=5):
		self.r = r
		self.c = c
		self.letters = [letters[i*c:i*c+c] for i in xrange(r)]
		self.owners = [owners[i*c:i*c+c] for i in xrange(r)]
	
	def setOwnerAt(self, r, c, owner):
		self.owners[r][c] = owner

	def getOwnerAt(self, r, c):
		return self.owners[r][c]
	
	def getLetterAt(self, r, c):
		return self.letters[r][c]
	
	# finds the max score of a word given board layout
	# prereq: word is in board
	def score(self, word):
		# note that if we do [[False]*self.c]*self.r, then we have five 
		# copies of the same object!!
		used = [[False for i in xrange(self.c)] for j in xrange(self.r)]

		def scoreAux(word, sc):
			if len(word) == 0:
				return sc
			maxScore = 0
			for r in xrange(self.r):
				for c in xrange(self.c):
					if not used[r][c] and self.letters[r][c] == word[0]:
						used[r][c] = True
						sc += int(self.owners[r][c] == '-' or self.owners[r][c] == 'r')
						maxScore = max(scoreAux(word[1:], sc), maxScore)
						sc -= int(self.owners[r][c] == '-' or self.owners[r][c] == 'r')
						used[r][c] = False
			return maxScore

		return scoreAux(word.upper(), 0)

# takes two lists of characters
# check if haystack contains needle
def contains(haystack, needle):
	haystack = sorted(haystack.upper())
	needle = sorted(needle.upper())
	if len(needle) > len(haystack):
		return False
	j = 0
	for i in xrange(len(needle)):
		while j < len(haystack) and haystack[j] < needle[i]:
			j += 1
		if j == len(haystack) or haystack[j] > needle[i]:
			return False
		elif haystack[j] == needle[i]:
			j += 1
	return True

# see if we can make words using the unused characters
# b: a Board instance
# wordl: a list of words
def attemptWin(b, wordl):
	unused = [b.letters[r][c] for r in xrange(b.r) for c in xrange(b.c) if b.owners[r][c] == '-']
	stripped = []
	for w in wordl:
		if all([c in w for c in unused]): # does not correctly handle repetitions in unused
			stripped.append(w)
	return greedy(b, stripped)

# b: a Board instance
# wordl: a list of words that are at least 3 chars long
# sample: the number of words to return
def greedy(b, wordl, sample=20):
	w = sorted(wordl, key=lambda a: -len(a))
	w = sorted(w[:sample], key=lambda a: -b.score(a))
	return w

def nicePrint(l):
	for x in l:
		print x

def main():
	f = open('TWL06.txt')
	print 'Enter word:',
	r = raw_input()
	print 'Enter owners:',
	o = raw_input()
	b = Board(r.upper(), o)
	wordl = []
	for l in f:
		l = l.strip()
		if len(l) > 2 and contains(r,l):
			wordl.append(l)

	result = attemptWin(b, wordl)
	if result:
		nicePrint(result)
	else:
		nicePrint(greedy(b, wordl, sample=30))

if __name__ == '__main__':
	main()
