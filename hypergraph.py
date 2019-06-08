#!/usr/bin/python3
import csv
import os


class Hypergraph(object):

    def __init__(self, tgt_dir, tgt_name, dat_file, dat_path="data"):
        self.tgt_dir = tgt_dir
        self.tgt_name = tgt_name
        self.dat_path = dat_path
        self.dat_file = dat_file

    def clean_airport_coords(self, write=False):
        airports = {}

        with open(os.path.join(self.dat_path, "AIRPORT_GPS_COORD.csv")) as gps_file:
            reader = csv.reader(gps_file, delimiter=',')

            for row in reader:
                airports[row[1]] = (row[6], row[7])

        sorted_airports = dict((k, airports[k]) for k in sorted(airports.keys()))

        if write:
            with open(os.path.join(self.dat_path, "master_coords.csv"), "w+") as gps_file:
                for k in sorted_airports.keys():
                    gps_file.write(k + "," + sorted_airports[k][0] + "," + sorted_airports[k][1] + "\n")

        return sorted_airports

    def get_found_nnumbers(self, tails, is_sorted=True):
        reg_tails = []
        with open(os.path.join(self.dat_path, "aircraft_info/MASTER.txt")) as reg_info:
            reg_tails = [x[0] for x in csv.reader(reg_info, delimiter=',')]

        reg_set = set(reg_tails)

        if is_sorted:
            return sorted(tails.intersection(reg_set))
        else:
            return tails.intersection(reg_set)

    def make_hgraph(self):
        graph = {}
        airports = set()
        tails = set()

        with open(os.path.join(self.dat_path, self.dat_file)) as data_file:
            reader = csv.reader(data_file, delimiter=',')

            _airports = []
            prev_tail = ""
            for tail_num, org, dest in reader:
                airports.add(org)
                airports.add(dest)
                if tail_num != prev_tail and _airports:
                    if len(tail_num) == 5:  # throw away invalid N-Numbers
                        tails.add(tail_num)
                    graph[prev_tail] = _airports
                    prev_tail = tail_num
                    _airports = []

                if not _airports or _airports[-1] != org:
                    _airports.append(org)
                _airports.append(dest)

        regs = {}
        tails = self.get_found_nnumbers(tails)
        with open(os.path.join(self.dat_path, "aircraft_info/MASTER.txt")) as reg_info:
            reader = csv.reader(reg_info, delimiter=',')
            for row in reader:
                if not tails:
                    break
                elif tails[0] == row[0]:
                    regs[tails[0]] = row[6]
                    tails.remove(tails[0])
            if tails:
                print("[WARNING] " + self.dat_file + ": Not all valid tails have been processed.")

        with open(os.path.join(self.tgt_dir, self.tgt_name + ".ids"), "w+") as acfts:
            for k, v in regs.items():
                acfts.write(k + " " + v + "\n")

        with open(os.path.join(self.tgt_dir, self.tgt_name + ".hgraph"), "w+") as hgraph:
            for v in graph.values():
                v_str = " ".join(v)
                res = str(len(v)) + " " + v_str + "\n"
                hgraph.write(res)

        locs = {}
        airports = sorted(airports)
        with open(os.path.join(self.dat_path, "L_AIRPORT_ID.csv")) as seq_file:
            reader = csv.reader(seq_file, delimiter=',')

            for seq, name in reader:
                if not airports:
                    break
                elif airports[0] == seq:
                    locs[name] = seq
                    airports.pop(0)

        port_names = locs.keys()

        gps_data = self.clean_airport_coords(True)
        for k, v in gps_data.items():
            for name in port_names:
                if name in k:
                    locs[name] = str(locs[name]) + " " + str(v)

        with open(os.path.join(self.tgt_dir, self.tgt_name + ".airports"), "w+") as apts:
            for k, v in locs.items():
                apts.write(v + " " + k + "\n")


if __name__ == "__main__":
    hg = Hypergraph("hypergraphs", "5_flights", "515819853_T_ONTIME.csv")
    hg.make_hgraph()
    hg = Hypergraph("hypergraphs", "8_flights", "839251150_T_ONTIME.csv")
    hg.make_hgraph()
