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
if len(sys.argv) == 3 and "resurrect" not in sys.argv[1]:
    delta = int(sys.argv[1])
    treshold = float(sys.argv[2])

elif len(sys.argv) == 4:
    if "resurrect" in sys.argv[2]:
        resurrect = True
        delta = int(sys.argv[1])
else:
    sys.stderr.write(
        "Usage: cat <stream> | python main.py <delta> <treshold> [--resurrect=<err_file>]\
        \n\n")
    sys.stderr.write("  --resurrect: Recover previous instance by providing\
    an stderr output \
    previous instance.\n\n")
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
    if not resurrect:
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

# Populate CliqueManager from err file
if resurrect:
    with open(sys.argv[3]) as error_file:
        for line in error_file:
            if line[0] == 'G':
                # Remove from S
                clique = line.split(" ")[2] + " " + line.split(" ")[3]
                nodes = line.split(" ")[2].split(",")
                duration = line.split(" ")[3].split("(")[0].split(",")
                c = Clique(
                    (frozenset(nodes), (int(
                        duration[0]), int(
                        duration[1]))))

                if c in Cm._S:
                    Cm._S.remove(c)

            elif line[0] == 'A':
                # Add to S and S_set
                clique = line.split(" ")[1] + " " + line.split(" ")[2]
                nodes = line.split(" ")[1].split(",")
                duration = line.split(" ")[2].split(",")
                c = Clique(
                    (frozenset(nodes), (int(
                        duration[0]), int(
                        duration[1]))))

                Cm._S.append(c)
                Cm._S_set.add(c)

            elif "maximal" in line:
                # Add to R
                clique = line.split(" ")[0] + " " + line.split(" ")[1]
                nodes = line.split(" ")[0].split(",")
                duration = line.split(" ")[1].split(",")
                c = Clique(
                    (frozenset(nodes), (int(
                        duration[0]), int(
                        duration[1]))))
                Cm._R.add(c)

            # Write original err line to be consistent
            sys.stderr.write(line)

# Restart execution
R = Cm.getDeltaCliques(delta, treshold)
sys.stdout.write("# delta = %d %d\n" % (delta))
Cm.printCliques()
