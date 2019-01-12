#!/usr/bin/python3
import csv
import os

def make_hgraph(graph_dir, dat_path, seq_path):
    graph = {}
    airports = set()
    tails = set()

    with open(dat_path) as data_file:
        reader = csv.reader(data_file, delimiter = ',')

        _airports = []
        prev_tail = ""
        for tail_num, org, dest in reader:
            airports.add(org)
            airports.add(dest)
            if tail_num != prev_tail and _airports:
                tails.add(tail_num)
                graph[prev_tail] = _airports
                prev_tail = tail_num
                _airports = []

            if not _airports or _airports[-1] != org:
                _airports.append(org)
            _airports.append(dest)

    regs = {}
    tails = sorted(tails)
    path = "data/aircraft_info/MASTER.txt"
    with open(path) as reg_info:
        reader = csv.reader(reg_info, delimiter = ',')
        for row in reader:
            if not tails:
                break
            elif tails[0] == row[0]:
                regs[tails[0]] = row[6]
                tails.remove(tails[0])
        if tails:
            print(tails)
    
    with open(os.path.join(graph_dir, "flights.ids"), "w+") as acfts:
        for k, v in regs.items():
            acfts.write(k + " " + v + "\n")

    with open(os.path.join(graph_dir, "flights.hgraph"), "w+") as hgraph:
        for v in graph.values():
            v_str = " ".join(v)
            res = str(len(v)) + " " + v_str + "\n"
            hgraph.write(res)
    
    locs = {}
    airports = sorted(airports)
    with open(seq_path) as seq_file:
        reader = csv.reader(seq_file, delimiter = ',')

        for seq, name in reader:
            if not airports:
                break
            elif airports[0] == seq:
                locs[seq] = name 
                airports.remove(seq)

    with open(os.path.join(graph_dir, "flights.airports"), "w+") as apts:
        for k, v in locs.items():
            apts.write(k + " " + v + "\n")

if __name__ == "__main__":
    make_hgraph("Hypergraph", "data/839251150_T_ONTIME.csv", "data/L_AIRPORT_ID.csv")
