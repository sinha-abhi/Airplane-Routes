# Creates a hypergraph representation of the airplane data using information from acquired data sets

import csv
import os

# final hypergraph, stored as: {plane number: [airports...]}
graph = {}

# read data file
data_file_path = "839251150_T_ONTIME.csv"
with open(os.path.join("data", data_file_path)) as data_file:
    reader = csv.reader(data_file, delimiter=',')

    airports = []
    prev_tail = ""
    for tail_num, org, dest, ignore in reader:
        if (tail_num != prev_tail) and (len(airports) > 0):
            graph[prev_tail] = airports
            prev_tail = tail_num
            airports = []

        if (len(airports) == 0) or (airports[-1] != org):
            airports.append(org)
        airports.append(dest)

with open("flights.hgraph", "w") as hgraph:
    for v in graph.values():
        v_str = " ".join(v)
        res = str(len(v)) + " " + v_str + "\n"
        hgraph.write(res)
