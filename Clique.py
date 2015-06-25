# -*-coding:utf8*-
import sys
import bisect


class Clique:

    def __init__(self, c, candidates=set([])):
        (X, (tb, te)) = c
        self._X = X
        self._tb = tb
        self._te = te
        self._candidates = candidates

    def __eq__(self, other):
        if self._X == other._X and self._tb == other._tb and self._te == other._te:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self._X, self._tb, self._te))

    def __str__(self):
        return ','.join(map(str, list(self._X))) + " " + \
            str(self._tb) + "," + str(self._te)

    def getAdjacentNodes(self, times, nodes, delta):
        if self._te - self._tb <= delta:
            for u in self._X:
                neighbors = nodes[u]
                for n in neighbors:
                    if len([i for i in times[frozenset([u,n])] if(i >= self._tb and i <= self._te)]) > 0:
                        self._candidates.add(n)

        self._candidates = self._candidates.difference(self._X)
        return self._candidates

    def isClique(self, times, node, delta):
        """ returns True if X(c) union node is a clique over tb;te, False otherwise"""

        for i in self._X:
            if frozenset([i, node]) not in times.keys():
                # Verifier que le lien existe
                sys.stderr.write("(%s, %s) does not exist\n" % (i, node))
                return False
            else:
                # Verifier qu'il apparaît tous les delta entre tb et te
                link = frozenset([i, node])
                time = times[link][bisect.bisect_left(times[link], self._tb):bisect.bisect_right(times[link], self._te)]
                if len(time) == 0:
                    return False
                time = [self._tb] + time + [self._te]
                #ict = [j - i for i, j in zip(time[:-1], time[1:])]
                for t in range(0, len(time)-1):
                    if time[t+1] - time[t] > delta:
                        return False
        return True

    def getTd(self, times, delta):
        # Pour chaque lien dans X, Récupérer dans T les temps x tq te-delta < x
        # < te. Si len(T) = 1, regarder si x est plus petit que le tmin déjà
        # connu.
        td = 0
        max_t = []
        for u in self._X:
            for v in self._X:
                link = frozenset([u, v])
                if link in times:
                    a = times[link][bisect.bisect_left(times[link], self._tb):bisect.bisect_right(times[link], self._te)]
                    if len(a) > 0:
                        max_t.append(max(a))
        if len(max_t) > 0:
            td = min(max_t)
        else:
            td = self._te - delta
        sys.stderr.write("    td = %d\n" % (td))
        return td

    def getTp(self, times, delta):
        # Pour chaque lien dans X, Récupérer dans T les temps x tq te-delta < x
        # < te. Si len(T) = 1, regarder si x est plus petit que le tmin déjà
        # connu.
        tp = 0
        min_t = []

        for u in self._X:
            for v in self._X:
                link = frozenset([u, v])
                if link in times:
                    a = times[link][bisect.bisect_left(times[link], self._tb):bisect.bisect_right(times[link], self._te)]
                    if len(a) > 0:
                        min_t.append(min(a))
        if len(min_t) > 0:
            tp = max(min_t)
        else:
            tp = self._tb + delta
        sys.stderr.write("    tp = %d\n" % (tp))
        return tp


if __name__ == '__main__':
    c = Clique((frozenset([1, 2, 3]), (1, 3)))
    print(c)
