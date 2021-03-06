import numpy as np
import time as t
import os
import pandas as pd
import csv

def find_and_write_labels(spec_path,midi_path,output_path):
    print("Reading data")
    start = t.time()
    spec = pd.read_csv(spec_path)
    midi = pd.read_csv(midi_path)
    elapsed = t.time() - start
    print("done reading data: " + "{0:.2f}".format(elapsed) + "s")
    midiSlices = []
    print("starting to calculate labels")
    start = t.time()
    print(spec.shape)
    for i in range(int(spec.shape[0])):
        midiRow = [0] * 128
        timeslice = float(spec.loc[i,"time in seconds"])
        midifiltered = midi.loc[(midi["Onset_s"] <= timeslice) & (midi["Onset_s"] + midi["Duration_s"]  >= timeslice),["Pitch_MIDI"]]
        if(midifiltered.size > 1):
            for data in midifiltered["Pitch_MIDI"]:
                midiRow[int(data)] = 1
        midiRow.insert(0,timeslice)
        midiSlices.append(midiRow)
        timeslice += 1
    elapsed = t.time() - start
    print("done calculating labels: " + "{0:.2f}".format(elapsed) + "s")
    print(len(midiSlices))

    print("Start writing csv file")
    start = t.time()
    header = "time in seconds"
    for value in range(128):
        header += "," + str(value)
    header += "\n"
    with open(output_path, "w", newline='') as labels_csv:
        labels_csv.write(header)
        wr = csv.writer(labels_csv, quoting=csv.QUOTE_NONE)
        wr.writerows(midiSlices)
        labels_csv.close()
    elapsed = t.time() - start
    print("Finished writing spectral csv file in: " + "{0:.2f}".format(elapsed) + "s")