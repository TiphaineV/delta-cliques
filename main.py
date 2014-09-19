from CliqueMaster import CliqueMaster
from Clique import Clique
import sys

Cm = CliqueMaster()
times = dict()
nodes = dict()
delta = int(sys.argv[1]) 
nb_lines = 0

for line in sys.stdin:
	contents = line.split(" ")
	t = int(contents[0])
	u = int(contents[1])
	v = int(contents[2])

	link = frozenset([u,v])
	time = (t,t)
	
	Cm.addClique(Clique((link, time)))
	
	# Populate data structures
	if not times.has_key(link):
		times[link] = []
	times[link].append(t)

        if not u in nodes:
		nodes[u] = set()

	if not v in nodes:
		nodes[v] = set()

	nodes[u].add(v)
	nodes[v].add(u)
	nb_lines = nb_lines + 1
Cm._times = times
Cm._nodes = nodes
sys.stderr.write("Processed " + str(nb_lines) + "from stdin\n")
R = Cm.getDeltaCliques(delta)
sys.stdout.write("# delta = %d\n" % (delta))
Cm.printCliques()	
