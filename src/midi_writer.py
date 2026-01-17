#!/usr/bin/python3
# midi_writer.py

from typing import (List, Dict, Tuple)
import struct
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MidiWriter:
    TICKS_PER_QUARTER = 480

    # MIDI meta-event constants
    META_END_OF_TRACK = b"\xFF\x2F\x00"
    META_TEMPO_PREFIX = b"\xFF\x51\x03"
    META_TIME_SIGNATURE_PREFIX = b"\xFF\x58\x04"
    META_TRACK_NAME = b"\xFF\x03"

    # Note - By convention, we can use:
    # 0x7F to denote 0x0111_1111 and 
    # 0x80 to denote 0x1000_0000

    # Internal classes:
    class _Track:
        def __init__(self) -> None:
            self._events: List[Tuple[int, bytes]] = []

        def add_event(self, tick: int, data: bytes) -> None:
            self._events.append((tick, data))

        def sort_events(self) -> None:
            self._events.sort(key=lambda e: e[0])
        
        @property
        def get_events(self) -> List[Tuple[int, bytes]]:
            return self._events
    
    # CTOR for the MidiWriter class
    def __init__(self) -> None:
        ''' CTOR '''
        self._tracks: List["MidiWriter._Track"] = []
        self._channel_programs: Dict[int, int] = {}

        self.ticks_per_quarter: int = 480
        self.tracks: List[Track] = []
        self.channel_program: Dict[int, int] = {}
    
    def add_track(self) -> int:
        ''' Explicitly add a new track. Returns its index. '''
        self._tracks.append(MidiWriter._Track())
        return len(self._tracks) - 1
    
    def _get_track(self, track_index: int) -> "_Track":
        ''' Expand the track list if I need it. '''
        while track_index >= len(self._tracks):
            self.add_track()
        return self._tracks[track_index]
    
    # MIDI events:
    def set_channel(self, **kwargs) -> None:
        channel = kwargs.get("channel", 0)
        program = kwargs.get("program", 0)

        if (channel < 0 or channel > 15):
            raise ValueError("Channel must be between 0-15")
        if (program < 0 or program > 127):
            raise ValueError("Program must be between 0-127")
        
        self._channel_programs[channel] = program
        event = bytes([
            0xC0 | (channel & 0x0F), 
            program & 0x7F
        ])

        # By convention, the program changes go on Track 0
        self._get_track(0).add_event(0, event)

    def add_bpm(self, **kwargs) -> None:
        ''' 
        Parameters:
            track: int
            start: int 
            bpm: int
        Return:
            None
        '''

        track = kwargs.get("track", 0)
        start = kwargs.get("start", 0)
        bpm = kwargs.get("bpm", 120)

        if (bpm <= 0):
            logger.warnning("Invalid BPM: {}".format(bpm))
            return

        tempo = 60000000 // bpm
        tempo_bytes = tempo.to_bytes(3, "big") # encodes the tempo bytes to big endian
        event = MidiWriter.META_TEMPO_PREFIX + tempo_bytes
        
        self._get_track(track).add_event(start, event)


    def add_time_signature(self, **kwargs) -> None:
        track = kwargs.get("track", 0)
        start = kwargs.get("start", 0)
        numerator = kwargs.get("numerator", 4)
        denominator = kwargs.get("denominator", 4)

        if (numerator <= 0) or (denominator & (denominator - 1)) != 0:
            msg = "Invalid time signature: {}\{}".format(numerator, denominator)
            logger.warning(msg)
        
        dd = 0 
        d = denominator 
        while d > 1:
            d >>= 1
            dd += 1
        cc = 24 # Midi clocks per metronome tick 
        bb = 8 # 32nd notes per quarter note

        event = MidiWriter.META_TIME_SIGNATURE_PREFIX + bytes([numerator, dd, cc, bb])
        self._get_track(track).add_event(start, event)

    def add_track_name(self, **kwargs) -> None:
        track = kwargs.get("track", 0)
        start = kwargs.get("start", 0)
        name = kwargs.get("name", "Track")
        
        # char* literal into memory, we read until we terminate the string with \0 null terminator 
        name_bytes = name.encode("ascii", errors="ignore")
        event = MidiWriter.META_TRACK_NAME + bytes([len(name_bytes)]) + name_bytes

        self._get_track(track).add_event(start, event)


    def add_note(self, **kwargs) -> None:
        '''
        Params:
            track       : int [0, ...)
            channel     : int [0, ...)
            start       : int [0, ...)
            duration    : int [0, ...)
            pitch       : int [0, 127]
            velocity    : int [0, 127]
            off_velocity: int [0, 127]
        '''
        
        # get params from user
        track = kwargs.get("track", 0) 
        channel = kwargs.get("channel", 0)
        start = kwargs.get("start", 0) # default start of the score
        duration = kwargs.get("duration", MidiWriter.TICKS_PER_QUARTER) # default note duration will be a quarter note.
        pitch = kwargs.get("pitch", 60) # default pitch middle C
        velocity = kwargs.get("velocity", 120) # default velocity will be fairly loud: 120 
        off_velocity = kwargs.get("off_velocity", 64)
        
        # keep a running list of mutally exclusive errors
        errors = []

        if track < 0:
            msg = "track: {} - needs to be a positive integer".format(track)
            errors.append(msg)
        if channel < 0:
            msg = "channel: {} - needs to be a positive integer".format(channel)
            errors.append(msg)
        if start < 0: 
            msg = "start: {} - needs to be a positive integer".format(start)
            errors.append(msg)
        if duration <= 0:
            msg = "duration: {} - needs to be a positive integer".format(duration)
            errors.append(msg)
        if pitch < 0 or pitch > 127:
            msg = "pitch: {}".format(pitch)
            errors.append(msg)
        if velocity < 0 or velocity > 127:
            msg = "velocity: {}".format(velocity)
            errors.append(msg)
        if off_velocity < 0 or off_velocity > 127:
            msg = "off_velocity: {}".format(off_velocity)
            errors.append(msg)
        
        # print all to log if errors occur
        if errors:
            msg = "Invalid params: {}".format(" | ".join(errors))
            logger.warn(msg)
            return

        # create the note on and off events:
        end = start + duration 
        note_on = bytes([
            0x90 | (channel & 0x0F),
            pitch & 0x7F,
            velocity & 0x7F
        ])
        note_off = bytes([
            0x80 | (channel & 0x0F),
            pitch & 0x7F,
            velocity & 0x7F
        ])
        track_instance = self._get_track(track)
        track_instance.add_event(start, note_on)
        track_instance.add_event(start, note_off)

    ################################################################################
    # Encoding stage:
    @staticmethod
    def encode_var_len(value: int) -> bytes:
        ''' Encode an integer as a MIDI variable-length quantity. '''

        buffer = []
        shifted = value & 0x7F 

        while (value := value >> 7):
            shifted <<= 8 
            shifted |= (value & 0x7F) | 0x80 

        while True:
            buffer.append(shifted & 0xFF)
            if shifted & 0x80:
                shifted >>= 8 
            else:
                break

        return bytes(buffer) 

    ################################################################################
    # File output:
    
    def save_as_midi(self, filename: str) -> None: 
        # sort events in each track:
        for track in self._tracks:
            track.sort_events() 
        
        output = bytearray()

        # header chunk 
        output += b"MThd"
        output += struct.pack(">I", 6)
        
        # designates multiple tracks or not
        fmt = 1 if len(self._tracks) > 1 else 0
        
        output += struct.pack(">HHH", fmt, len(self._tracks), MidiWriter.TICKS_PER_QUARTER)
        for track in self._tracks:
            track_data = bytearray()
            last_tick = 0

            for tick, data in track._events:
                delta = tick - last_tick 
                last_tick = tick
                track_data += self.encode_var_len(delta)
                track_data += data 

            track_data += self.encode_var_len(0)
            track_data += MidiWriter.META_END_OF_TRACK

            output += b"MTrk"
            output += struct.pack(">I", len(track_data))
            output += track_data 

        try:
            with open(filename, "wb") as file:
                file.write(output)
        except Exception as e:
            msg = "Error: {}".format(e)
            logger.error(msg)
            return
        
        logger.info("Saved MIDI file: {}".format(filename))

