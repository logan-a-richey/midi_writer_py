#!/usr/bin/python3
# midi_writer.py

from typing import List, Dict, Tuple
import struct
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MIDI meta-event constants
META_END_OF_TRACK = bytes([0xFF, 0x2F, 0x00])
META_TEMPO_PREFIX = bytes([0xFF, 0x51, 0x03])
META_TIME_SIGNATURE_PREFIX = bytes([0xFF, 0x58, 0x04])

class Track:
    ''' Represents a single MIDI track, storing events as (tick, event_bytes) pairs. '''
    def __init__(self) -> None:
        self.events: List[Tuple[int, bytes]] = []

    def add_event(self, tick: int, event_bytes: bytes) -> None:
        self.events.append((tick, event_bytes))

    def sort_events(self) -> None:
        self.events.sort(key=lambda ev: ev[0])

class MidiWriter:
    '''
    A simple MIDI file writer using 480 ticks per quarter note.

    Methods:
        add_track() -> int
        set_channel(channel=0, program=0)
        add_bpm(track=0, start=0, bpm=120)
        add_note(track, channel, start, duration, pitch, velocity)
        add_time_signature(track, start, numerator, denominator)
        add_track_name(track, name, start=0)
        save(output_filename)
    '''

    def __init__(self) -> None:
        self.ticks_per_quarter: int = 480
        self.tracks: List[Track] = []
        self.channel_program: Dict[int, int] = {}

    def encode_var_len(self, value: int) -> bytes:
        ''' Encode an integer as a MIDI variable-length quantity. '''
        buffer = []
        buffer.append(value & 0x7F)
        value >>= 7
        while value:
            buffer.append((value & 0x7F) | 0x80)
            value >>= 7
        buffer.reverse()
        return bytes(buffer)

    def add_track(self) -> int:
        ''' Add a new track. Returns its index. '''
        track = Track()
        self.tracks.append(track)
        return len(self.tracks) - 1

    def _get_track(self, track_idx: int) -> Track:
        while track_idx >= len(self.tracks):
            self.add_track()
        return self.tracks[track_idx]

    def set_channel(self, channel: int, program: int) -> None:
        ''' Set the instrument (program) for a channel. '''
        self.channel_program[channel] = program
        track0 = self._get_track(0)
        event_bytes = bytes([0xC0 | (channel & 0x0F), program & 0x7F])
        track0.add_event(0, event_bytes)

    def add_bpm(self, track: int = 0, start: int = 0, bpm: int = 120) -> None:
        if track < 0 or start < 0 or bpm <= 0:
            logger.warning("Could not add BPM: track=%d, start=%d, bpm=%d", track, start, bpm)
            return
        tempo = int(60000000 / bpm)
        tempo_bytes = tempo.to_bytes(3, byteorder="big")
        meta_event = META_TEMPO_PREFIX + tempo_bytes
        trk = self._get_track(track)
        trk.add_event(start, meta_event)

    def add_time_signature(self, track: int, start: int, numerator: int, denominator: int):
        if track < 0 or start < 0 or numerator <= 0 or denominator not in [1, 2, 4, 8, 16, 32, 64]:
            logger.warning("Invalid time signature: track=%d, start=%d, numerator=%d, denominator=%d",
                           track, start, numerator, denominator)
            return
        dd = 0
        denom = denominator
        while denom > 1:
            denom >>= 1
            dd += 1
        cc = 24  # Default MIDI ticks per metronome click
        bb = 8   # Default number of 32nd notes per MIDI quarter note
        event_bytes = META_TIME_SIGNATURE_PREFIX + bytes([numerator, dd, cc, bb])
        trk = self._get_track(track)
        trk.add_event(start, event_bytes)

    def add_track_name(self, track: int, name: str, start: int = 0):
        name_bytes = name.encode('ascii')
        event_bytes = bytes([0xFF, 0x03, len(name_bytes)]) + name_bytes
        trk = self._get_track(track)
        trk.add_event(start, event_bytes)

    def add_note(self, track: int, channel: int, start: int, duration: int, pitch: int, velocity: int, off_velocity: int = 64) -> None:
        if track < 0 or channel < 0 or start < 0 or duration <= 0 or not (0 <= velocity <= 127):
            logger.warning("Could not add note: track=%d, channel=%d, start=%d, duration=%d, pitch=%d, velocity=%d",
                           track, channel, start, duration, pitch, velocity)
            return
        start_tick = int(start)
        end_tick = int(start + duration)
        trk = self._get_track(track)
        note_on = bytes([0x90 | (channel & 0x0F), pitch & 0x7F, velocity & 0x7F])
        note_off = bytes([0x80 | (channel & 0x0F), pitch & 0x7F, off_velocity & 0x7F])
        trk.add_event(start_tick, note_on)
        trk.add_event(end_tick, note_off)

    def save(self, output_filename: str):
        ''' Write data to .mid file '''
        for trk in self.tracks:
            trk.sort_events()
        num_tracks = len(self.tracks)
        header_chunk_type = b"MThd"
        header_length = 6
        midi_format = 1 if num_tracks > 1 else 0
        header_data = struct.pack(">hhh", midi_format, num_tracks, self.ticks_per_quarter)
        header_chunk = header_chunk_type + struct.pack(">I", header_length) + header_data
        track_chunks = b""
        for trk in self.tracks:
            track_data = bytearray()
            prev_tick = 0
            for tick, event in trk.events:
                delta_ticks = tick - prev_tick
                prev_tick = tick
                track_data += self.encode_var_len(delta_ticks)
                track_data += event
            track_data += self.encode_var_len(0)
            track_data += META_END_OF_TRACK
            track_chunk = b"MTrk" + struct.pack(">I", len(track_data)) + track_data
            track_chunks += track_chunk
        full_data = header_chunk + track_chunks
        with open(output_filename, "wb") as f:
            f.write(full_data)
        logger.info("Successfully created '%s'.", output_filename)

################################################################################

if __name__ == "__main__":
    # example usage 
    myMidi = MidiWriter()
    myMidi.add_bpm(track=0, start=0, bpm=120)
    myMidi.add_time_signature(track=0, start=0, numerator=3, denominator=8)
    myMidi.set_channel(channel=0, program=0)
    myMidi.add_track_name(0, "C Major Scale")
    notes = [60, 62, 64, 65, 67, 69, 71, 72]
    for beat, pitch in enumerate(notes):
        myMidi.add_note(0, 0, beat * 480, 480, pitch, 120)
    myMidi.save("test_scale.mid")
    exit(0)

