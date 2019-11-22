#!/usr/bin/python3
import csv
import os

class FlightHypergraph(object):
    def __init__(self, tgt_dir, tgt_name, dat_file, dat_path="data"):
        self.tgt_dir = tgt_dir
        self.tgt_name = tgt_name
        self.dat_path = dat_path
        self.dat_file = dat_file

        # data
        self.airports = None
        self.graph = None
        self.tails = None

    def clean_airport_coords(self, write=False):
        _airports = dict() 
        with open(os.path.join(self.dat_path, "AIRPORT_GPS_COORD.csv")) as gps_file:
            reader = csv.reader(gps_file, delimiter=',')
            for row in reader:
                _airports[row[1]] = (row[6], row[7])
        airports = dict((k, _airports[k]) for k in sorted(_airports.keys()))
        if write:
            with open(os.path.join(self.dat_path, "master_coords.csv"), "w+") as gps_file:
                for k in airports.keys():
                    gps_file.write(k + "," + airports[k][0] + "," + airports[k][1] + "\n")
        return airports 

    def get_found_nnumbers(self, tails, sort=True):
        _registered = list()
        with open(os.path.join(self.dat_path, "aircraft_info/MASTER.txt")) as reg_info:
            _registered = [x[0] for x in csv.reader(reg_info, delimiter=',')]
        registered = set(_registered)
        inter = tails.intersection(registered)
        return sorted(inter) if sort else inter

    def load_data(self):
        self.airports = set()
        self.graph = dict()
        self.tails = set()

        with open(os.path.join(self.dat_path, self.dat_file)) as data_file:
            reader = csv.reader(data_file, delimiter=',')
            _airports = list()
            prev_tail = ""
            next(reader) # skip header
            for tail_num, org, dest in reader:
                self.airports.add(org)
                self.airports.add(dest)
                if tail_num != prev_tail and _airports:
                    self.tails.add(tail_num)
                    self.graph[prev_tail] = _airports
                    prev_tail = tail_num
                    _airports = []
                if not _airports or _airports[-1] != org:
                    _airports.append(org)
                _airports.append(dest)

    def load_airports(self, airports, _sorted):
        locs = dict() 
        airports = sorted(airports) if not _sorted else airports
        with open(os.path.join(self.dat_path, "L_AIRPORT_ID.csv")) as seq_file:
            reader = csv.reader(seq_file, delimiter=',')
            for seq, name in reader:
                if not airports:
                    break
                elif airports[0] == seq:
                    locs[name] = seq
                    airports.pop(0)
        return locs

    def make_hgraph(self):
        """
        Stores a hypergraph representation of the data to a file.

        .hgraph - file extension
            Each line begins with the number of airports in the hyperedge, followed
            by a list of airports, indexed from 0 to n-1 (n is the total number
            of airports).
        .ids
            Flight id (N-Number) and airline.
        .airports
            Name, code and GPS coordinates for each airport.
        """
        if self.airports is None or self.graph is None or self.tails is None:
            self.load_data()

        regs = dict()
        tails = self.get_found_nnumbers(self.tails)
        with open(os.path.join(self.dat_path, "aircraft_info/MASTER.txt")) as reg_info:
            reader = csv.reader(reg_info, delimiter=',')
            for row in reader:
                if not tails:
                    break
                elif tails[0] == row[0]:
                    regs[tails[0]] = row[6]
                    tails.remove(tails[0])
            if tails:
                print("[WARNING]", self.dat_file, ": Not all valid tails have been processed.")

        with open(os.path.join(self.tgt_dir, self.tgt_name + ".ids"), "w+") as acfts:
            for k, v in regs.items():
                acfts.write(k + " " + v + "\n")

        with open(os.path.join(self.tgt_dir, self.tgt_name + ".hgraph"), "w+") as hgraph:
            for v in self.graph.values():
                v_str = " ".join(v)
                res = str(len(v)) + " " + v_str + "\n"
                hgraph.write(res)

        locs = self.load_airports(self.airports, False)
        port_names = locs.keys()
        gps_data = self.clean_airport_coords(False)
        for k, v in gps_data.items():
            for name in port_names:
                if name in k:
                    locs[name] = str(locs[name]) + " " + str(v)

        with open(os.path.join(self.tgt_dir, self.tgt_name + ".airports"), "w+") as apts:
            for k, v in locs.items():
                apts.write(v + " " + k + "\n")

    def graph(self, edge_cardinality):
        pass


if __name__ == "__main__":
    hg = FlightHypergraph("hypergraphs", "5_flights", "515819853_T_ONTIME.csv")
    hg.make_hgraph()
    # hg = FlightHypergraph("hypergraphs", "8_flights", "839251150_T_ONTIME.csv")
    # hg.make_hgraph()

