from CliqueMaster import CliqueMaster
from Clique import Clique
import sys

# Initiate
Cm = CliqueMaster()
times = dict()
nodes = dict()
nb_lines = 0
resurrect = False

# Read arguments from command line
if len(sys.argv) == 2:
    delta = int(sys.argv[1])
else:
    sys.stderr.write(
        "Usage: cat <stream> | python main.py <int:delta>\
        \n\n")
    sys.exit(1)

# Read stream
for line in sys.stdin:
    contents = line.split(" ")
    t = int(contents[0])
    u = contents[1].strip()
    v = contents[2].strip()

    link = frozenset([u, v])
    time = (t, t)

    # This a new instance
    Cm.addClique(Clique((link, time), set([])))

    # Populate data structures
    if link not in times:
        times[link] = []
    times[link].append(t)

    if u not in nodes:
        nodes[u] = set()

    if v not in nodes:
        nodes[v] = set()

    nodes[u].add(v)
    nodes[v].add(u)
    nb_lines = nb_lines + 1
Cm._times = times
Cm._nodes = nodes
sys.stderr.write("Processed " + str(nb_lines) + " from stdin\n")

# Restart execution
R = Cm.getDeltaCliques(delta, treshold)
sys.stdout.write("# delta = %d %d\n" % (delta))
Cm.printCliques()
