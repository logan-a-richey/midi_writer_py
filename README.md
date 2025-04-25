# midi_writer_py (README)
- lightweight Python module to create MIDI files.

## Overview
- `MidiWriter` is a lightweight Python class designed to generate and save MIDI files.
- It provides an easy-to-use interface for adding tracks, setting channels, specifying tempo, and inserting MIDI note events.

## Features
- add track
- add program channel mapping
- add note (track, channel, pitch, start, duration, pitch, velocity)
- add time signatures
- add bpm changes
- save and write to file (MIDI binary)
- uses MIDI standard of 480 ticks per quarter note.

## Installation
- simply import the `MidiWriter` class with your Python project:
`from midi_writer import MidiWriter`
- create an instance of the MidiWriter object to call its functions.

