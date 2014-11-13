#-*-coding:utf8*-
import sys
import bisect

class Clique:
	def __init__(self, c):
		(X,(tb,te)) = c
		self._X = X
		self._tb = tb
		self._te = te
                self._candidates = set()
	
	def __eq__(self, other):
		if self._X == other._X and self._tb == other._tb and self._te == other._te:
			return True
		else:
			return False

	def __hash__(self):
		return hash((self._X, self._tb, self._te))

	def __str__(self):
		return ','.join(map(str, list(self._X)))  + " " + str(self._tb) + "," + str(self._te)
	
	def getAdjacentNodes(self, times, nodes, delta):
            if self._te - self._tb <= delta:
                self._candidates = set()

                for u in self._X:
                    neighbors = nodes[u]
                    for n in neighbors:
                        # On regarde si le lien est apparu entre tb et te
                        is_present = False
                        if self._tb in times[frozenset([u,n])]:
				self._candidates.add(n)

                        if self._te in times[frozenset([u,n])]:
                        	self._candidates.add(n)


                    self._candidates = self._candidates.difference(self._X)
	    return self._candidates

	def getFirstTInInterval(self, times, nodes, td, delta):
		# Plus petit t entre te et td + delta impliquant (u,v) ?
		t =  None
		# Bien extraire tous les noeuds de la clique et du voisinage de chaque noeud de la clique (c'est ici qu'on fait grossir le temps pour pouvoir ajouter des noeuds)
		# Get all links implying at least one of X's nodes.
		candidates = set()
		for u in self._X:
			for n_u in nodes[u]:
				link = frozenset([u,n_u])

				if link in times:
					candidates.add(link)

		# Get the intercontact times in [te;td+delta]
		for candidate in candidates:
			sys.stderr.write("c is " + str(candidate) + "\n")              
			sys.stderr.write("tt is " + str(times[candidate]) + "\n")              
			index = bisect.bisect_right(times[candidate], self._te)
			sys.stderr.write(str(index) + "/" + str(len(times[candidate]))+ "\n")

			if len(times[candidate]) == 1 and index == 1 and times[candidate][index-1] <= td + delta:
				if times[candidate][index - 1] > self._te:
					if t>times[candidate][index-1] or t==None: 
						t = times[candidate][index-1]
			elif index < len(times[candidate]) and times[candidate][index] <= td + delta:
				if times[candidate][index - 1] > self._te:
					if t>times[candidate][index] or t==None:
						t = times[candidate][index]

		sys.stderr.write("    new_t = %s\n" % (str(t)))
		return t

	def isClique(self, times, node, delta):
		""" returns True if X(c) union node is a clique over tb;te, False otherwise"""

		for i in self._X:
			if frozenset([i, node]) not in times.keys():
				# Verifier que le lien existe
				sys.stderr.write("(%d, %d) does not exist\n" % (i, node))
				return False
			else:
				# Verifier qu'il apparaît tous les delta entre tb et te
				link = frozenset([i,node])
				time = [x for x in times[link] if(x >= self._tb and x <= self._te)]
				if len(time)==0:
					return False
				time = [self._tb] + time + [self._te]
				ict = [j - i for i,j in zip(time[:-1], time[1:])]
				for t in ict:
					if t > delta:
						return False
		return True

	def getLastTInInterval(self, times, nodes, tp, delta):
		# Plus petit t entre tb et tp - delta impliquant (u,v) ? 
		t = None
		# Bien extraire tous les noeuds de la clique et du voisinage de chaque noeud de la clique (c'est ici qu'on fait grossir le temps pour pouvoir ajouter des noeuds)
		
		# Get all links implying at least one of X's nodes.
		candidates = set()
		for u in self._X:
			for n_u in nodes[u]:
				link = frozenset([u,n_u])
				if link in times:
					candidates.add(link)
		# Get the intercontact times in [tp - delta; tb]
		for candidate in candidates:
                        index = bisect.bisect_left(times[candidate], self._tb)
                        index = index - 1
                        
                        if index >= 0 and times[candidate][index] >= tp - delta:
				if  t<times[candidate][index] or t==None:
                            		t = times[candidate][index]

		sys.stderr.write("    new_t = %s\n" % (str(t)))
		return t

	def getTd(self, times, delta):
		# Pour chaque lien dans X, Récupérer dans T les temps x tq te-delta < x < te. Si len(T) = 1, regarder si x est plus petit que le tmin déjà connu.
		td = 0
		max_t = []
		for u in self._X:
			for v in self._X:
				link = frozenset([u,v])
				if link in times:
					a =	([x for x in times[link] if(x >= max(self._tb, self._te - delta) and x <= self._te)])
					if len(a) > 0:
						max_t.append(max(a))
		if len(max_t) > 0:
			td = min(max_t)
		else:
			td = self._te - delta
		sys.stderr.write("    td = %d\n" % (td))
		return td
	
	def getTp(self, times, delta):
		# Pour chaque lien dans X, Récupérer dans T les temps x tq te-delta < x < te. Si len(T) = 1, regarder si x est plus petit que le tmin déjà connu.
		tp = 0
		min_t = []

		for u in self._X:
			for v in self._X:
				link = frozenset([u,v])
				if link in times:
					a =	([x for x in times[link] if(x <= min(self._te, self._tb + delta) and x >= self._tb)])
					if len(a) > 0:
						min_t.append(min(a))
		if len(min_t) > 0:
			tp = max(min_t)
		else:
			tp = self._tb + delta
		sys.stderr.write("    tp = %d\n" % (tp))
		return tp
	

if __name__ == '__main__':
	c = Clique((frozenset([1,2,3]), (1,3)))
	print(c)
