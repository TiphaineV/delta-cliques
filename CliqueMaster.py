#-*-coding:utf8*-

import sys
from collections import deque
from Clique import Clique

class CliqueMaster:
	
	def __init__(self):
		self._S = deque()
		self._S_set = set()
		self._R = set()
		self._times = dict()
		self._nodes = dict()

	def addClique(self, c):
		""" Adds a clique to S, checking beforehand that this clique is not already present in S. """
		if not c in self._S_set:
			#self._S.appendleft(c)
                        self._S.append(c)
			self._S_set.add(c)

	def getClique(self):
		c = self._S.pop()
		sys.stderr.write("\nGetting clique " + str(c) + "\n")
		return c

	def getDeltaCliques(self, delta):
		""" Returns a set of maximal cliques. """

		while len(self._S) != 0:
                        sys.stderr.write("S:"+ str(len(self._S)) + "\n")
			c = self.getClique()
			is_max = True

			# Grow time on the right side
			td = c.getTd(self._times, delta)
			if c._te != td + delta:
				new_t = c.getFirstTInInterval(self._times, self._nodes, td, delta)
				if new_t is not None:
					c_add = Clique((c._X, (c._tb, new_t)))
					sys.stderr.write("Adding " + str(c_add) + " (time extension)\n")
					self.addClique(c_add)
				else:
					c_add = Clique((c._X, (c._tb, td + delta)))
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (time delta extension)\n")
				is_max = False
			else:
				sys.stderr.write(str(c) + " cannot grow on the right side\n")

			# Grow time on the left side 
			tp = c.getTp(self._times, delta)
			if c._tb != tp - delta:
				new_t = c.getLastTInInterval(self._times, self._nodes, tp, delta)
				if new_t is not None:
					c_add = Clique((c._X, (new_t , c._te)))
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + "(left time extension)\n")
				else:
					c_add = Clique((c._X, (tp - delta, c._te)))
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (left time delta extension)\n")
				is_max = False
			else:
				sys.stderr.write(str(c) + " cannot grow on the left side\n")

			# Grow node set
			candidates = c.getAdjacentNodes(self._times, self._nodes, delta)
			sys.stderr.write("    Candidates : %s.\n" % (str(candidates)))

			for node in candidates:
				if c.isClique(self._times, node, delta):
					Xnew = set(c._X).union([node])
					c_add = Clique((frozenset(Xnew), (c._tb, c._te)))
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (node extension)\n")
					is_max = False

			if is_max:
				sys.stderr.write(str(c) + " is maximal\n")
				self._R.add(c)
		return self._R

	def printCliques(self):
		for c in self._R:
			sys.stdout.write(str(c) + "\n")
	
	def __str__(self):
		msg = ""
		for c in self._R:
			msg += str(c) + "\n"
		return msg
