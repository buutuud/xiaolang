import collections
import logging
import pipes
import re
import subprocess
import tempfile
from client import diagnose
from client import plugin

if not diagnose.check_executable('espeak'):
    raise ImportError("espeak executable not found!")


RE_PATTERN = re.compile(r'(?P<pty>\d+)\s+' +
                        r'(?P<lang>[a-z-]+)\s+' +
                        r'(?P<gender>[MF-])\s+' +
                        r'(?P<name>[\w-]+)\s+\S+\s+' +
                        r'(?P<other>(?:\([a-z-]+\s+\d+\))*)')
RE_OTHER = re.compile(r'\((?P<lang>[a-z-]+)\s+(?P<pty>\d+)\)')

Voice = collections.namedtuple(
    'Voice', ['name', 'gender', 'priority', 'language'])


class EspeakTTSPlugin(plugin.TTSPlugin):
    """
    Uses the eSpeak speech synthesizer included in the Jasper disk image
    Requires espeak to be available
    """

    def __init__(self, *args, **kwargs):
        plugin.TTSPlugin.__init__(self, *args, **kwargs)

        self._logger = logging.getLogger(__name__)

        self.voice = self.profile.get('Espeak', 'Voice', 'zh')
        self._logger.info("Using voice '%s'.", self.voice)

        self.pitch_adjustment = self.profile.getint('Espeak', 'PitchAdjustment', 40)
        self.words_per_minute = self.profile.getint('Espeak', 'WordsPerMinute', 160)

    def get_voices(self):
        output = subprocess.check_output(['espeak', '--voices'])
        output += subprocess.check_output(['espeak', '--voices=mbrola'])
        voices = []
        for pty, lang, gender, name, other in RE_PATTERN.findall(output):
            voices.append(Voice(name=name, gender=gender,
                                priority=int(pty), language=lang))
            if len(other) > 0:
                for lang2, pty2 in RE_OTHER.findall(other):
                    voices.append(Voice(name=name, gender=gender,
                                        priority=int(pty2), language=lang2))
        return sorted(voices, key=lambda voice: voice.priority)

    def say(self, phrase):
        if isinstance(phrase, unicode):
            phrase = phrase.encode('utf8')
        with tempfile.SpooledTemporaryFile() as out_f:
            cmd = ['espeak', '-v', self.voice,
                             '-p', self.pitch_adjustment,
                             '-s', self.words_per_minute,
                             '--stdout',
                             phrase]
            cmd = [str(x) for x in cmd]
            self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                         for arg in cmd]))
            subprocess.call(cmd, stdout=out_f)
            out_f.seek(0)
            data = out_f.read()
            return data
