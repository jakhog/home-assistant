"""
"""
import logging
from homeassistant.components.remote import RemoteDevice
from homeassistant.const import DEVICE_DEFAULT_NAME
from homeassistant.components.remote import (ATTR_NUM_REPEATS, ATTR_DELAY_SECS, DEFAULT_NUM_REPEATS, DEFAULT_DELAY_SECS)


DEPENDENCIES = ['arduino']

_LOGGER = logging.getLogger(__name__)

COMMANDS = {
    'PowerOn': [2, 30, 1],
    'PowerOff': [2, 29, 1],
    # Menus
    'Setup': [12, 160, 0],
    'Mode': [12, 216, 0],
    'Up': [12, 92, 0],
    'Down': [12, 91, 0],
    'Right': [2, 221, 0],
    'Left': [12, 127, 0],
    # Input selection
    'InputAnalog': [2, 220, 0],
    'InputAux': [2, 198, 0],
    'InputCd': [2, 196, 0],
    'InputTuner': [2, 197, 0],
    'InputDvd': [2, 227, 0],
    'InputTape': [2, 210, 0],
    'InputTv': [2, 201, 0],
    'InputVaux': [2, 204, 0],
    'InputVcr': [2, 205, 0],
    'InputMode': [12, 182, 0],
    # Sound control
    'VolUp': [2, 241, 0],
    'VolDown': [2, 242, 0],
    'Mute': [2, 240, 0],
    'Stereo': [2, 231, 0],
    'Standard': [2, 228, 0],
    'DspSim': [2, 25, 0],
    'SpeakerToggle': [2, 237, 0],
    'VirtualSurround': [4, 137, 0],
    'Cinema': [4, 149, 0],
    'Music': [4, 150, 0],
    'FiveChannelStereo': [12, 87, 0],
    'SurroundBack': [12, 130, 0],
    'Direct': [12, 158, 0],
    'SoundParameter': [12, 161, 0],
    # Play controls
    'Play': [8, 160, 0],
    'Pause': [8, 157, 0],
    'Rewind': [8, 155, 0],
    'FastForward': [8, 154, 0],
    'Stop': [8, 161, 0],
    'ChapterNext': [8, 152, 0],
    'ChapterPrev': [8, 153, 0],
    'ChapterSelect': [12, 175, 0],
    # Receiver specific
    'Status': [2, 222, 0],
    'TestTone': [2, 234, 0],
    'VideoSelect': [2, 216, 0],
    'Memory': [12, 204, 0],
    'Dimmer': [12, 223, 0],
    'Shift': [12, 205, 0]
}

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the Arduino remote."""
    from homeassistant.components.arduino import BOARD
    add_devices_callback([ArduinoRemote(BOARD)])
    return True

class ArduinoRemote(RemoteDevice):
    """Representation of Arduino remote."""
    
    def __init__(self, board):
        """Initialize HarmonyRemote class."""
        self._name = 'Arduino Remote'
        self._state = None
        self._board = board

    @property
    def should_poll(self):
        """No polling needed for an Arduino remote."""
        return False

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def is_on(self):
        """Return true if remote is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the remote on."""
        self._state = True
        self.send_command(['PowerOn'])
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the remote off."""
        self._state = False
        self.send_command(['PowerOff'])
        self.schedule_update_ha_state()

    def send_command(self, command, **kwargs):
        """Send a command to a device."""
        num_repeats = kwargs.get(ATTR_NUM_REPEATS, DEFAULT_NUM_REPEATS)
        delay = kwargs.get(ATTR_DELAY_SECS, DEFAULT_DELAY_SECS)
        self.arduino_send_command(command, num_repeats, delay)
        self.schedule_update_ha_state()

    def arduino_send_command(self, command, num_repeats, delay):
        if (self._board is not None):
            cmd = command[0]
            data = COMMANDS.get(cmd, None)
            if (data is None):
                _LOGGER.warning("Unrecognized command %s", cmd)
            else:
                _LOGGER.debug("Sending command %s -> %s", cmd, str(data))
                self._board._board._command_handler.send_sysex(0x01, data)
