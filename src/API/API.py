import os
import pandas as pd
from API import fingering
from API import hand
from API import scoreparser

def process_file(input_file, output_file):
    # INPUT_FILE = "Fr_Elise.mxl"
    # INPUT_FILE = "Senbonzakura.mxl"
    # OUTPUT_FILE = "output.mxl"
    DATA_DIR = "/Users/nckasman/Downloads/HowdyHack/dataset/PianoFingeringDataset_v1.02/FingeringFiles"
    
    # These inputs will be an API endpoint
    #Get music data from music21 lib
    # score = scoreparser.Score(path = input_file)
    score = scoreparser.Score(path = input_file)

    left_hand = hand.Hand("L")
    right_hand = hand.Hand("R")

    #Construct the Hidden Markov Chain from training data
    directory = os.listdir(DATA_DIR)

    pig_format = [
        "id",
        "onset",
        "offset",
        "pitch",
        "onsetvel",
        "offsetvel",
        "hand",
        "fingernum",
    ]

    left_notes = list()
    right_notes = list()
    for file in directory:
        path = DATA_DIR + "/" + file
        data = pd.read_csv(path, sep="\t", header=0, names=pig_format)

        if data.fingernum.dtype == object:
            data.fingernum = data.fingernum.apply(
                lambda x: x.split("_")[0]
            ).astype("int")


        # Split data into left and right hand (negative(-) indicates left finger)
        left_notes.append(data[data.fingernum < 0])
        right_notes.append(data[data.fingernum > 0])

    left_hand.build_from_data(left_notes)
    right_hand.build_from_data(right_notes)

    # 0 indicates right hand (treble clef), 1 indicates left (bass clef)
    right_part = score.build_note_info(0)
    left_part = score.build_note_info(1)

    #Calculate diffs
    right_part["time_diff"] = right_part.time.diff()
    left_part["time_diff"] = left_part.time.diff()
    right_part["pitch_diff"] = fingering.note_to_diff(right_part)
    left_part["pitch_diff"] = fingering.note_to_diff(left_part)

    #Run algorithm to get optimal fingering from Hidden Markov Model
    right_num = right_hand.decoding(right_part)
    left_num = left_hand.decoding(left_part)

    right_part["finger_num"] = right_num[1:]
    left_part["finger_num"] = left_num[1:]

    #Add numbers to file
    score.add_fingernum(0, right_part)
    score.add_fingernum(1, left_part)

    # Output file
    score.write_on(output_file)
