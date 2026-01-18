#!/usr/bin/env python3
# examples.py
# Demonstrates use of my flexible MidiWriter library class.

# system modules
from __future__ import annotations

import os 
from typing import List, Tuple, Dict
import sys
sys.dont_write_bytecode = True

# user modules
from midi_writer import MidiWriter
from config import Config

# create output directory if it doesn't exist already
ROOT_DIR = os.getcwd()
OUTPUT_DIR = os.path.join(ROOT_DIR, Config.OUTPUT_DIR_NAME)
os.makedirs(OUTPUT_DIR, exist_ok=True)

################################################################################

def example_scale():
    output_file_name = Config.EXAMPLE_SCALE
    
    # initialize MidiWriter 
    my_midi_writer = MidiWriter()
    my_midi_writer.add_bpm(start=0, bpm=90)
    my_midi_writer.add_time_signature(start=0, numerator=3, denominator=8)
    my_midi_writer.set_channel(channel=0, program=0)
    my_midi_writer.add_track_name(track=0, name="C Major Scale")

    # create some notes
    notes = [60, 62, 64, 65, 67, 69, 71, 72]
    for midi_step, pitch in enumerate(notes):
        my_start = MidiWriter.TICKS_PER_QUARTER * midi_step 
        my_duration = MidiWriter.TICKS_PER_QUARTER 

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
    
    output_file_path = os.path.join(OUTPUT_DIR, output_file_name)
    my_midi_writer.save_as_midi(output_file_path)

def example_twinkle_star():
    output_file_name = Config.EXAMPLE_TWINKLE
    
    # initialize MidiWriter 
    my_midi_writer = MidiWriter()
    my_midi_writer.add_bpm(start=0, bpm=130)
    my_midi_writer.add_time_signature(start=0, numerator=3, denominator=4)
    my_midi_writer.set_channel(channel=0, program=0)
    my_midi_writer.add_track_name(track=0, name="Twinkle Star")
    
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

    subdiv = MidiWriter.TICKS_PER_QUARTER // 2
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
        
    output_file_path = os.path.join(OUTPUT_DIR, output_file_name)
    my_midi_writer.save_as_midi(output_file_path)

def example_chords():
    output_file_name = Config.EXAMPLE_CHORDS
    
    # initialize MidiWriter 
    my_midi_writer = MidiWriter()
    my_midi_writer.add_bpm(start=0, bpm=120)
    my_midi_writer.add_time_signature(start=0, numerator=4, denominator=4)
    my_midi_writer.set_channel(channel=0, program=0)
    my_midi_writer.add_track_name(track=0, name="Block Chords")
    
    note_mapping = {
        "c": 0,
        "d": 2,
        "e": 4,
        "f": 5,
        "g": 7,
        "a": 9,
        "b": 11
    }
    chords = ["C", "Dm", "Em", "F", "G7", "Am", "Bmb5", "C"]

    for midi_step, chord in enumerate(chords):
        notes_in_chord = []

        third_offset = 4 
        fifth_offset = 7 
        has_seventh = False

        if "b5" in chord:
            fifth_offset -= 1
        if "m" in chord:
            third_offset -= 1
        
        root_pitch = note_mapping.get(chord[0].lower(), 60)
        third_pitch = root_pitch + third_offset 
        fifth_pitch = root_pitch + fifth_offset 

        notes_in_chord.append(root_pitch)
        notes_in_chord.append(third_pitch)
        notes_in_chord.append(fifth_pitch)
        if "7" in chord:
            has_seventh = True
            seventh_pitch = root_pitch + 10
            notes_in_chord.append(seventh_pitch)
        
        notes_in_one_octave = [note % 12 + 60 for note in notes_in_chord]
        
        my_start = 480 * midi_step
        my_duration = 480

        my_midi_writer.add_note(
            track=0,
            channel=0, # default: drums channel is 9
            start=my_start,
            duration=my_duration,
            pitch=notes_in_chord[0] + 48,
            velocity=100
        )
        for note in notes_in_one_octave:
            my_midi_writer.add_note(
                track=0,
                channel=0, # default: drums channel is 9
                start=my_start,
                duration=my_duration,
                pitch=note,
                velocity=100
            )
    
    output_file_path = os.path.join(OUTPUT_DIR, output_file_name)
    my_midi_writer.save_as_midi(output_file_path)

def example_overlapping_voices():
    output_file_name = Config.EXAMPLE_OVERLAPPING
    
    # initialize MidiWriter 
    my_midi_writer = MidiWriter()
    my_midi_writer.add_bpm(start=0, bpm=120)
    my_midi_writer.add_time_signature(start=0, numerator=4, denominator=4)
    my_midi_writer.set_channel(channel=0, program=0)
    my_midi_writer.add_track_name(track=0, name="Overlapping Voices")
    
    notes = [60, 64, 67, 71]
    for midi_step, note in enumerate(notes):
        # each note happens on the subdivision
        my_start = 480 * midi_step 
        
        # make 2 overlapping notes at once
        my_duration = 480 * 3 
        
        my_midi_writer.add_note(
            track=0, 
            channel=0, 
            start=my_start, 
            duration=my_duration,
            pitch=note
        )

    output_file_path = os.path.join(OUTPUT_DIR, output_file_name)
    my_midi_writer.save_as_midi(output_file_path)

class DrumTest:
    def __init__(self):
        self.drum_mapping = {
            "kick_drum": 35,
            "snare_drum_rim": 37,
            "snare_drum": 38,
            "cymbal_hihat_closed": 42,
            "cymbal_hihat_open": 46,
            "cymbal_crash1": 49,
            "cymbal_crash2": 57,
            "cymbal_china": 52,
            "cymbal_ride": 51,
            "cymbal_ride_bell": 53,
            "cymbal_splash": 55,
            "tom2": 43,
            "tom3": 45,
            "tom4": 47,
            "tom5": 50,
            "tambourine": 54,
            "cowbell": 56
        }

    def create_drum_midi(self, drum_data: List[Tuple[str, str]], tempo: int, output_file_name: str) -> None:
        # initialize MidiWriter 
        my_midi_writer = MidiWriter()
        my_midi_writer.add_bpm(start=0, bpm=tempo)
        my_midi_writer.add_time_signature(start=0, numerator=4, denominator=4)
        my_midi_writer.set_channel(channel=0, program=0)
        my_midi_writer.add_track_name(name="Generated Drums")

        DRUM_CHANNEL = 9
        SUBDIV = 480 // 4 

        for drum_name, drum_pattern in drum_data:
            drum_pitch = self.drum_mapping.get(drum_name, self.drum_mapping["cymbal_hihat_closed"])
            midi_step = 0
            for c in drum_pattern:
                my_start = midi_step * SUBDIV 
                if c == "x":
                    my_midi_writer.add_note(
                        track=0,
                        channel=DRUM_CHANNEL,
                        start=my_start,
                        duration=SUBDIV,
                        pitch=drum_pitch
                    )
                if c != "|":
                    midi_step += 1

        output_file_path = os.path.join(OUTPUT_DIR, output_file_name)
        my_midi_writer.save_as_midi(output_file_path)

    def example_amen_drums(self):
        data = [
            ("cymbal_crash1", "................|................|................|..........x.....|"),
            ("cymbal_ride", "x.x.x.x.x.x.x.x.|x.x.x.x.x.x.x.x.|x.x.x.x.x.x.x.x.|x.x.x.x.x...x.x.|"),
            ("snare_drum", "....x.......x...|....x.......x...|....x.........x.|....x.........x.|"),
            ("snare_drum_rim", ".......x.x.....x|.......x.x.....x|.......x.x......|.x.....x.x......|"),
            ("kick_drum", "x.........xx....|x.........xx....|x.x.......x.....|..xx......x.....|"),
        ]
        tempo = 170
        output_file_name = Config.EXAMPLE_DRUMS_AMEN
        self.create_drum_midi(data, tempo, output_file_name)

    def example_disco_drums(self):
        data = [
            ("cymbal_crash1", "|x...............|................|................|................|x...............|"),
            ("cymbal_ride", "|................|................|x...x...x...x...|................|................|"),
            ("cymbal_ride_bell", "|................|................|..x...x...x...x.|................|................|"),
            ("cymbal_hihat_closed", "|....xx.xxx.xxx.x|xx.xxx.xxx.xxx.x|................|................|................|"),
            ("cymbal_hihat_open", "|......x...x...x.|..x...x...x...x.|................|................|................|"),
            ("tom5", "|................|................|................|xxx.............|................|"),
            ("tom4", "|................|................|................|...xxx..........|................|"),
            ("tom3", "|................|................|................|......xxx.......|................|"),
            ("tom2", "|................|................|................|.........xxx....|................|"),
            ("cowbell", "|x...x...x...x...|x...x...x...x...|x...x...x...x...|x...x...x...x...|x...............|"),
            ("snare_drum", "|....x.......x..x|....x.......xxxx|...x..x....x..x.|............xxxx|................|"),
            ("kick_drum", "|x.....x...x..x..|x.....x...x..x..|x.....x...x..x..|x...x...x...x...|x...............|"),
        ]
        tempo = 125
        output_file_name = Config.EXAMPLE_DRUMS_DISCO
        self.create_drum_midi(data, tempo, output_file_name)

def example_drums():
    d = DrumTest()
    d.example_amen_drums()
    d.example_disco_drums()

def example_multiple_tracks():
    # initialize MidiWriter 
    my_midi_writer = MidiWriter()
    my_midi_writer.add_bpm(start=0, bpm=120)
    my_midi_writer.add_time_signature(start=0, numerator=4, denominator=4)

    STRINGS = 48
    my_midi_writer.set_channel(channel=0, program=STRINGS)
    my_midi_writer.set_channel(channel=1, program=STRINGS)
    
    NUM_VOICES = 8
    THREE_BEATS = 480 * 3
    for idx in range(NUM_VOICES):
        my_midi_writer.add_track_name(track=idx, name="Sinister Strings {}".format(idx))
    
    # stack a dimished chord
    notes = [60 + 3 * i for i in range(NUM_VOICES)]
    my_duration = THREE_BEATS
    for track_idx, note in enumerate(notes):
        # alternate channels so that musescore does not join similar channels
        channel_idx = track_idx % 2 
        
        my_midi_writer.add_note(
            track=track_idx, 
            channel=channel_idx, 
            pitch=note, 
            start=480, 
            duration=my_duration
        )

    output_file_name = Config.EXAMPLE_MULTI_TRACK
    output_file_path = os.path.join(OUTPUT_DIR, output_file_name)
    my_midi_writer.save_as_midi(output_file_path)

