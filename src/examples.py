#!/usr/bin/env python3
# examples.py
# Demonstrates use of my flexible MidiWriter library class.

from midi_writer import MidiWriter
import os 

import sys
sys.dont_write_bytecode = True

ROOT_DIR = os.getcwd()
OUTPUT_DIR = os.path.join(ROOT_DIR, "midi_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def example_scale():
    # initialize MidiWriter 
    my_midi_writer = MidiWriter()
    my_midi_writer.add_bpm(start=0, bpm=90)
    my_midi_writer.add_time_signature(start=0, numerator=3, denominator=8)
    my_midi_writer.set_channel(channel=0, program=0)
    my_midi_writer.add_track_name(name="C Major Scale")

    # create some notes
    notes = [60, 62, 64, 65, 67, 69, 71, 72]
    for midi_step, pitch in enumerate(notes):
        my_start = 480 * midi_step 
        my_duration = 480 

        # all variables have good default values    
        # here, I show using all of them
        my_midi_writer.add_note(
            track=0, 
            channel=0,
            start=my_start,
            duration=my_duration, 
            pitch=pitch,
            velcoity=120
        )
    
    output_file_name = "test_c_major_scale.mid"
    output_file_path = os.path.join(OUTPUT_DIR, output_file_name)
    my_midi_writer.save_as_midi(output_file_path)

def example_twinkle_star():
    # initialize MidiWriter 
    my_midi_writer = MidiWriter()
    my_midi_writer.add_bpm(start=0, bpm=130)
    my_midi_writer.add_time_signature(start=0, numerator=3, denominator=4)
    my_midi_writer.set_channel(channel=0, program=0)
    my_midi_writer.add_track_name(name="Twinkle Star")
    
    # create some notes:
    note_mapping = {
        "c": 60,
        "d": 62,
        "e": 64,
        "f": 65,
        "g": 67,
        "a": 69,
        "b": 71
    }

    subdiv = 480 // 2
    song = "".join([
        "ccggaag.ffeeddc.", 
        "ggffeed.ggffeed.", 
        "ccggaag.ffeeddc."
    ])
    
    for midi_step, c in enumerate(song):
        if c == '.':
            continue

        my_start = subdiv * midi_step
        my_duration = subdiv 
        my_pitch = note_mapping.get(c, 60)
        
        my_midi_writer.add_note(
            start=my_start, 
            pitch=my_pitch,
            duration=my_duration
        )
        
    output_file_name = "test_twinkle_star.mid"
    output_file_path = os.path.join(OUTPUT_DIR, output_file_name)
    my_midi_writer.save_as_midi(output_file_path)

