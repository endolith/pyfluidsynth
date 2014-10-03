from ctypes import byref, c_char_p, c_double, c_int
import sys

from ._bindings import FLUID_INT_TYPE, FLUID_NUM_TYPE, FLUID_STR_TYPE, handle

GM_prog_name = {
# Piano
    0: 'Acoustic Grand Piano',
    1: 'Bright Acoustic Piano',
    2: 'Electric Grand Piano',
    3: 'Honky-tonk Piano',
    4: 'Electric Piano 1',
    5: 'Electric Piano 2',
    6: 'Harpsichord',
    7: 'Clavinet',

# Chromatic Percussion
    8: 'Celesta',
    9: 'Glockenspiel',
    10: 'Music Box',
    11: 'Vibraphone',
    12: 'Marimba',
    13: 'Xylophone',
    14: 'Tubular Bells',
    15: 'Dulcimer',

# Organ
    16: 'Drawbar Organ',
    17: 'Percussive Organ',
    18: 'Rock Organ',
    19: 'Church Organ',
    20: 'Reed Organ',
    21: 'Accordion',
    22: 'Harmonica',
    23: 'Tango Accordion',

# Guitar
    24: 'Acoustic Guitar (nylon)',
    25: 'Acoustic Guitar (steel)',
    26: 'Electric Guitar (jazz)',
    27: 'Electric Guitar (clean)',
    28: 'Electric Guitar (muted)',
    29: 'Overdriven Guitar',
    30: 'Distortion Guitar',
    31: 'Guitar Harmonics',

# Bass
    32: 'Acoustic Bass',
    33: 'Electric Bass (finger)',
    34: 'Electric Bass (pick)',
    35: 'Fretless Bass',
    36: 'Slap Bass 1',
    37: 'Slap Bass 2',
    38: 'Synth Bass 1',
    39: 'Synth Bass 2',

# Strings
    40: 'Violin',
    41: 'Viola',
    42: 'Cello',
    43: 'Contrabass',
    44: 'Tremolo Strings',
    45: 'Pizzicato Strings',
    46: 'Orchestral Harp',
    47: 'Timpani',

# Ensemble
    48: 'String Ensemble 1',
    49: 'String Ensemble 2',
    50: 'Synth Strings 1',
    51: 'Synth Strings 2',
    52: 'Choir Aahs',
    53: 'Voice Oohs',
    54: 'Synth Choir',
    55: 'Orchestra Hit',

# Brass
    56: 'Trumpet',
    57: 'Trombone',
    58: 'Tuba',
    59: 'Muted Trumpet',
    60: 'French Horn',
    61: 'Brass Section',
    62: 'Synth Brass 1',
    63: 'Synth Brass 2',

# Reed
    64: 'Soprano Sax',
    65: 'Alto Sax',
    66: 'Tenor Sax',
    67: 'Baritone Sax',
    68: 'Oboe',
    69: 'English Horn',
    70: 'Bassoon',
    71: 'Clarinet',

# Pipe
    72: 'Piccolo',
    73: 'Flute',
    74: 'Recorder',
    75: 'Pan Flute',
    76: 'Blown bottle',
    77: 'Shakuhachi',
    78: 'Whistle',
    79: 'Ocarina',

# Synth Lead
    80: 'Lead 1 (square)',
    81: 'Lead 2 (sawtooth)',
    82: 'Lead 3 (calliope)',
    83: 'Lead 4 chiff',
    84: 'Lead 5 (charang)',
    85: 'Lead 6 (voice)',
    86: 'Lead 7 (fifths)',
    87: 'Lead 8 (bass + lead)',

# Synth Pad
    88: 'Pad 1 (new age)',
    89: 'Pad 2 (warm)',
    90: 'Pad 3 (polysynth)',
    91: 'Pad 4 (choir)',
    92: 'Pad 5 (bowed)',
    93: 'Pad 6 (metallic)',
    94: 'Pad 7 (halo)',
    95: 'Pad 8 (sweep)',

# Synth Effects
    96: 'FX 1 (rain)',
    97: 'FX 2 (soundtrack)',
    98: 'FX 3 (crystal)',
    99: 'FX 4 (atmosphere)',
    100: 'FX 5 (brightness)',
    101: 'FX 6 (goblins)',
    102: 'FX 7 (echoes)',
    103: 'FX 8 (sci-fi)',

# Ethnic
    104: 'Sitar',
    105: 'Banjo',
    106: 'Shamisen',
    107: 'Koto',
    108: 'Kalimba',
    109: 'Bagpipe',
    110: 'Fiddle',
    111: 'Shanai',

# Percussive
    112: 'Tinkle Bell',
    113: 'Agogo',
    114: 'Steel Drums',
    115: 'Woodblock',
    116: 'Taiko Drum',
    117: 'Melodic Tom',
    118: 'Synth Drum',
    119: 'Reverse Cymbal',

# Sound effects
    120: 'Guitar Fret Noise',
    121: 'Breath Noise',
    122: 'Seashore',
    123: 'Bird Tweet',
    124: 'Telephone Ring',
    125: 'Helicopter',
    126: 'Applause',
    127: 'Gunshot',
    }

GM_prog_num = {v:k for k, v in GM_prog_name.items()}



def coerce_to_int(s):
    """
    Turn a string into an integer.
    """

    try:
        return int(s)
    except ValueError:
        return int(s.lower() not in ("false", "no", "off"))


class FluidError(Exception):
    """
    Something bad happened.
    """


class FluidSettings(object):

    def __init__(self):
        self.settings = handle.new_fluid_settings()
        self.quality = "med"

        # Quirk: For Linux, ALSA is preferred over JACK only if explictly set.
        if "linux" in sys.platform:
            self["audio.driver"] = "alsa"

    def __del__(self):
        handle.delete_fluid_settings(self.settings)

    def __getitem__(self, key):
        key_type = handle.fluid_settings_get_type(self.settings, key)
        if key_type == FLUID_NUM_TYPE:
            v = c_double()
            f = handle.fluid_settings_getnum
        elif key_type == FLUID_INT_TYPE:
            v = c_int()
            f = handle.fluid_settings_getint
        elif key_type == FLUID_STR_TYPE:
            v = c_char_p()
            f = handle.fluid_settings_getstr
        else:
            raise KeyError(key)

        if f(self.settings, key, byref(v)):
            return v.value
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        key_type = handle.fluid_settings_get_type(self.settings, key)
        if key_type == FLUID_STR_TYPE:
            if not handle.fluid_settings_setstr(self.settings, key, value):
                raise KeyError(key)
        else:
            # Coerce to integer before going further
            value = coerce_to_int(value)
            if key_type == FLUID_NUM_TYPE:
                if not handle.fluid_settings_setnum(self.settings, key, value):
                    raise KeyError
            elif key_type == FLUID_INT_TYPE:
                if not handle.fluid_settings_setint(self.settings, key, value):
                    raise KeyError
            else:
                raise KeyError

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, value):
        self._quality = value
        if value == "low":
            self["synth.chorus.active"] = "off"
            self["synth.reverb.active"] = "off"
            self["synth.sample-rate"] = 22050
        elif value == "med":
            self["synth.chorus.active"] = "off"
            self["synth.reverb.active"] = "on"
            self["synth.sample-rate"] = 44100
        elif value == "high":
            self["synth.chorus.active"] = "on"
            self["synth.reverb.active"] = "on"
            self["synth.sample-rate"] = 44100


class FluidSynth(object):
    """
    Parameters
    ----------
    settings : FluidSettings object
    """

    def __init__(self, settings):
        self._sf_dict = {}
        self.synth = handle.new_fluid_synth(settings.settings)
        self.settings = settings

    def __del__(self):
        failed = []
        for sf in self._sf_dict:
            if handle.fluid_synth_sfunload(self.synth, self._sf_dict[sf],
                                           True):
                failed.append(sf)
        handle.delete_fluid_synth(self.synth)

        if failed:
            raise FluidError("Couldn't unload soundfonts: %s" % failed)

    def load_soundfont(self, sf, reload_presets=True):
        """
        Load a SoundFont file (filename is interpreted by SoundFont loaders).

        The newly loaded SoundFont will be put on top of the SoundFont stack.
        Presets are searched starting from the SoundFont on the top of the
        stack, working the way down the stack until a preset is found.

        Parameters
        ----------
        sf : string
            Filename of a soundfont to load
        reload_presets : bool (optional)
            True to re-assign presets for all MIDI channels (default)
        """
        if sf in self._sf_dict:
            if (handle.fluid_synth_sfreload(self.synth, self._sf_dict[sf])
                    == -1):
                raise FluidError("Couldn't reload soundfont %s" % sf)
        else:
            i = handle.fluid_synth_sfload(self.synth, sf, reload_presets)
            if i == -1:
                raise FluidError("Couldn't load soundfont %s" % sf)
            else:
                self._sf_dict[sf] = i

    def unload_soundfont(self, sf, reload_presets=True):
        """
        Unload a SoundFont.

        Parameters
        ----------
        sf
            ID of SoundFont to unload
        reload_presets : bool
            True to re-assign presets for all MIDI channels (default)
        """
        if sf not in self._sf_dict:
            raise FluidError("Soundfont %s was never loaded" % sf)
        if handle.fluid_synth_sfunload(self.synth, self._sf_dict[sf],
                                       reload_presets):
            raise FluidError("Couldn't unload soundfont %s" % sf)
        else:
            del self._sf_dict[sf]

    def noteon(self, channel, pitch, velocity):
        """
        Send a note-on event to a FluidSynth object.

        Parameters
        ----------
        channel : int
            MIDI channel number (0 to MIDI channel count - 1)
        pitch : int or float
            MIDI note number (0-127 or float from 0.0 to 1.0)
        velocity : int
            MIDI velocity (0-127, 0 = noteoff)
        """
        if isinstance(velocity, float):
            velocity = int(velocity * 127)
        handle.fluid_synth_noteon(self.synth, channel, pitch, velocity)

    def noteoff(self, channel, pitch):
        """
        Send a note-off event to a FluidSynth object.

        Parameters
        ----------
        channel : int
            MIDI channel number (0 to MIDI channel count - 1)
        pitch : int
            MIDI note number (0-127)
        """
        handle.fluid_synth_noteoff(self.synth, channel, pitch)

    def cc(self, channel, control, value):
        """
        Send a MIDI controller event on a MIDI channel.

        Parameters
        ----------
        channel : int
            MIDI channel number (0 to MIDI channel count - 1)
        control : int
            MIDI controller number (0-127)
        value : int
            MIDI controller value (0-127)
        """
        handle.fluid_synth_cc(self.synth, channel, control, value)

    control_change = cc

    def pitch_bend(self, channel, value):
        """
        Set the MIDI pitch bend controller value on a MIDI channel.

        Parameters
        ----------
        channel : int
            MIDI channel number (0 to MIDI channel count - 1)
        value : int
            MIDI pitch bend value (0-16383 with 8192 being center)
        """
        handle.fluid_synth_pitch_bend(self.synth, channel, value)

    def pitch_wheel_sens(self, channel, value):
        """
        Set MIDI pitch wheel sensitivity on a MIDI channel.

        Parameters
        ----------
        channel : int
            MIDI channel number (0 to MIDI channel count - 1)
        value : int
            Pitch wheel sensitivity value in semitones
        """
        handle.fluid_synth_pitch_wheel_sens(self.synth, channel, value)

    pitch_wheel_sensitivity = pitch_wheel_sens

    def program_change(self, channel, program):
        """
        Send a program change event on a MIDI channel.

        Parameters
        ----------
        channel : int
            MIDI channel number (0 to MIDI channel count - 1)
        program : int
            MIDI program number (0-127)
            or a string like 'Dulcimer'
        """
        if isinstance(program, basestring):
            program = GM_prog_num[program]
        handle.fluid_synth_program_change(self.synth, channel, program)

    def bank_select(self, channel, bank):
        """
        Set instrument bank number on a MIDI channel.

        Parameters
        ----------
        channel : int
            MIDI channel number (0 to MIDI channel count - 1)
        bank : int
            MIDI bank number
        """
        handle.fluid_synth_bank_select(self.synth, channel, bank)


class FluidAudioDriver(object):
    """
    Parameters
    ----------
    settings : FluidSynth object
    """

    def __init__(self, synth):
        self.audio_driver = handle.new_fluid_audio_driver(
            synth.settings.settings, synth.synth)
        self.synth = synth

    def __del__(self):
        handle.delete_fluid_audio_driver(self.audio_driver)


class FluidPlayer(object):
    """
    Parameters
    ----------
    settings : FluidSynth object
    """

    paused = True

    def __init__(self, synth):
        self.player = handle.new_fluid_player(synth.synth)
        self.synth = synth

    def __del__(self):
        self.stop()
        self.join()

        if handle.delete_fluid_player(self.player):
            raise FluidError("Couldn't delete fluid player!")

    def add(self, midi):
        handle.fluid_player_add(self.player, midi)

    def play(self, midi=None):
        if midi:
            self.add(midi)
        handle.fluid_player_play(self.player)
        self.paused = False

    def stop(self):
        handle.fluid_player_stop(self.player)
        self.paused = True

    def join(self):
        handle.fluid_player_join(self.player)

    def pause(self):
        self.play() if self.paused else self.stop()
        self.paused = not self.paused


class FluidEvent(object):

    source = -1
    dest = -1

    def __init__(self):
        self.event = handle.new_fluid_event()

    def __del__(self):
        handle.delete_fluid_event(self.event)

    @property
    def source(self):
        return handle.fluid_event_get_source(self.event)

    @source.setter
    def source(self, value):
        handle.fluid_event_set_source(self.event, value)

    @property
    def dest(self):
        return handle.fluid_event_get_dest(self.event)

    @dest.setter
    def dest(self, value):
        handle.fluid_event_set_dest(self.event, value)

    def timer(self):
        # XXX should support callbacks
        handle.fluid_event_timer(self.event, None)

    def volume(self, channel, value):
        handle.fluid_event_volume(self.event, channel, value)

    def note(self, channel, key, velocity, duration):
        handle.fluid_event_note(self.event, channel, key, velocity, duration)

    def noteon(self, channel, key, velocity):
        handle.fluid_event_noteon(self.event, channel, key, velocity)

    def noteoff(self, channel, key):
        handle.fluid_event_noteoff(self.event, channel, key)

    def pitch_bend(self, channel, pitch):
        handle.fluid_event_pitch_bend(self.event, channel, pitch)

    def pitch_sens(self, channel, amount):
        handle.fluid_event_pitch_wheelsens(self.event, channel, amount)

    def pc(self, a, b):
        handle.fluid_event_program_change(self.event, a, b)


class FluidSequencer(dict):

    _bpm = 120
    _tpb = 120

    def __init__(self, *synths):
        super(FluidSequencer, self).__init__()

        self.seq = handle.new_fluid_sequencer()

        if synths:
            for synth in synths:
                self.add_synth(synth)

        self._update_tps()

    def __del__(self):
        handle.delete_fluid_sequencer(self.seq)

    def __delitem__(self, key):
        id, name = self[key]
        handle.fluid_sequencer_unregister_client(self.seq, id)

        super(FluidSequencer, self).__delitem__(key)

    @property
    def beats_per_minute(self):
        return self._bpm

    @beats_per_minute.setter
    def beats_per_minute(self, value):
        self._bpm = value
        self._update_tps()

    @property
    def ticks_per_beat(self):
        return self._tpb

    @ticks_per_beat.setter
    def ticks_per_beat(self, value):
        self._tpb = value
        self._update_tps()

    @property
    def ticks_per_second(self):
        return handle.fluid_sequencer_get_time_scale(self.seq)

    @ticks_per_second.setter
    def ticks_per_second(self, value):
        handle.fluid_sequencer_set_time_scale(self.seq, value)

    @property
    def ticks(self):
        return handle.fluid_sequencer_get_tick(self.seq)

    def _update_tps(self):
        self.ticks_per_second = (self._tpb * self._bpm) / 60.0

    def is_dest(self, id):
        return bool(handle.fluid_sequencer_client_is_dest(self.seq, id))

    def add_synth(self, synth):
        id = handle.fluid_sequencer_register_fluidsynth(self.seq, synth.synth)
        name = handle.fluid_sequencer_get_client_name(self.seq, id)

        self[synth] = id, name

        return id, name

    def send(self, event, timestamp, absolute=True):
        handle.fluid_sequencer_send_at(self.seq, event.event, timestamp,
                                       absolute)

    def send_right_now(self, event):
        handle.fluid_sequencer_send_now(self.seq, event.event)
