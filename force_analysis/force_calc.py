#!/usr/bin/env python

import pandas as pd
import re, sys, os
import numpy as np
import csv

def calc_force(data, distance, term):
    force = -1.0*data[distance]['0.0010'][term] + 8.0*data[distance]['0.0005'][term] - 8.0*data[distance]['-0.0005'][term] + data[distance]['-0.0010'][term]
    force /= -12.0*0.0005
    return force

df = pd.read_csv('result/eda2_force_decomp/EDA2.csv')
display(df)

data_eql = {}
with open('result/eda2_force_decomp/EDA2.csv') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    next(csvreader)
    for row in csvreader:
        l = re.search("(\S+)_frzgeom_bond_(\S+)", row[0])
        molname, shift = l.group(1), l.group(2)
        if molname not in data_eql:
            data_eql[molname] = {}
        data_eql[molname][shift] = {}
        data_eql[molname][shift]["elec"] = float(row[1])
        data_eql[molname][shift]["pauli"] = float(row[2])
        data_eql[molname][shift]["disp"] = float(row[3])
csvfile.close()
fw = open('result/frz_forces_eql.csv', 'w')
fw.write('name,elec,pauli,disp\n')
for molname in data_eql:
    force_elec = calc_force(data_eql, molname, 'elec')
    force_pauli = calc_force(data_eql, molname, 'pauli')
    force_disp = calc_force(data_eql, molname, 'disp')
    fw.write('%s,%.8f,%.8f,%.8f\n' %(molname, force_elec, force_pauli, force_disp))
fw.close()
