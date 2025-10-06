# MidiWriter Python
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

## License
MIT License (MIT)

Copyright (c) 2025 LoganARichey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
