# Imports
import board
from kmk.keys import KC, make_key
from kmk.kmk_keyboard import KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.handlers.sequences import send_string, simple_key_sequence
from rotaryio import IncrementalEncoder

# OLED IMPORTS
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_sh1107

# OTHER IMPORTS
from kmk.internal_state import InternalState

# OLED CONFIG
displayio.release_displays()
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 128
HEIGHT = 64
BORDER = 0
display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)
#splash = displayio.Group(max_size=10)
splash = displayio.Group(max_size=10)
display.show(splash)
color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
splash.append(inner_sprite)
#text1 = "112345621234563123456"
text2 = "NumPad"
#text_area1 = label.Label(terminalio.FONT, text=text1, sacle=1, color=0xFFFFFF, x=9, y=5)
text_area2 = label.Label(terminalio.FONT, text=text2, scale=1, color=0xFFFFFF, x=0, y=5)
#splash.append(text_area1)
splash.append(text_area2)
display.brightness=.1
#display.refresh(target_frames_per_second=60, minimum_frames_per_second=60)

# Keyboard setup
keyboard = KMKKeyboard()
keyboard.debug_enabled = False

# Rotary encoder
keyboard.rotaries = [IncrementalEncoder(board.A1, board.A0)]

# Define colums/rows
keyboard.col_pins = (board.D24, board.D23, board.D0, board.D1)
keyboard.row_pins = (board.A2, board.A3, board.A4, board.A5, board.D25)
keyboard.diode_orientation = DiodeOrientation.ROWS

# Custom keycodes
_______ = KC.TRNS
XXXXXXX = KC.NO

# Macros
TIAM12 = send_string('this is a macro')




### TEST AREA
def which_layer(*args, **kwargs):
    global text_area2
    splash.remove(text_area2)
    if InternalState.active_layers == [0]:
        text2 = "NumPad"
    elif InternalState.active_layers == [1]:
        text2 = "Layers:\n7| --- 8| --- 9| --- \n4| AFF 5| VSC 6| ---  \n1| NUM 2| NAV 3| ALT"
    elif InternalState.active_layers == [2]:
        text2 = "AltPad:\n7| --- 8| --- 9| ---  \n4| --- 5| --- 6| ---  \n1| Num 2| Nav 3| Aff"
    elif InternalState.active_layers == [3]:
        text2 = "Affinity \n7| --- 8| --- 9| ---  \n4| CPY 5|  ^  6| PST  \n1|  <  2|  V  3|  >"
    elif InternalState.active_layers == [4]:
        text2 = "VS Code \n7| SAV 8| --- 9| ----  \n4| CPY 5|  ^  6| PST  \n1|  <  2|  V  3|  >"
    elif InternalState.active_layers == [5]:
        text2 = "NavPad \n7| NUM 8| NAV 9| LAY  \n4| CPY 5|  ^  6| PST  \n1|  <  2|  V  3|  >"
    text_area2 = label.Label(terminalio.FONT, text=text2, scale=1, color=0xFFFFFF, x=5, y=5)
    #splash.append(text_area1)
    splash.append(text_area2)

LAYERKEY = make_key(on_press=which_layer)

# Layers
NUMPAD = simple_key_sequence((KC.TO(0),LAYERKEY))
LAYERS = simple_key_sequence((KC.TO(1),LAYERKEY))
ALTPAD = simple_key_sequence((KC.TO(2),LAYERKEY))
AFFINITY = simple_key_sequence((KC.TO(3),LAYERKEY))
VSCODE = simple_key_sequence((KC.TO(4),LAYERKEY))
NAVPAD = simple_key_sequence((KC.TO(5),LAYERKEY))
# Keymaps by layer
keyboard.keymap = [
    # NUMPAD (layer 0)
     [ 
        LAYERS,  KC.PSLS,  KC.PAST,     KC.PMNS,    KC.VOLU, 
        KC.N7,   KC.N8,    KC.N9,       KC.PPLS,    KC.VOLD,
        KC.N4,   KC.N5,    KC.N6,       XXXXXXX,    XXXXXXX,
        KC.N1,   KC.N2,    KC.N3,       KC.ENTER,   XXXXXXX,
        KC.N0,   XXXXXXX,  KC.DOT,      XXXXXXX,    XXXXXXX,
     ],
    # LAYERS (layer 1)
     [ 
        NUMPAD,     NUMPAD,     NUMPAD,     NUMPAD,     KC.VOLU,
        NUMPAD,     NUMPAD,     AFFINITY,   NUMPAD,     KC.VOLD,
        AFFINITY,   VSCODE,     NUMPAD,     XXXXXXX,    XXXXXXX,
        NUMPAD,     NAVPAD,     ALTPAD,     NUMPAD,     XXXXXXX,
        NUMPAD,     XXXXXXX,    NUMPAD,     XXXXXXX,    XXXXXXX,
     ], 
    # ALTPAD (layer 2)
     [ 
        LAYERS,     NUMPAD,     NUMPAD,     NUMPAD,     KC.VOLU,
        NUMPAD,     NUMPAD,     AFFINITY,   NUMPAD,     KC.VOLD,
        AFFINITY,   VSCODE,     NUMPAD,     XXXXXXX,    XXXXXXX,
        NUMPAD,     NAVPAD,     ALTPAD,     NUMPAD,     XXXXXXX,
        NUMPAD,     XXXXXXX,    NUMPAD,     XXXXXXX,    XXXXXXX,
     ], 
    # AFFINITY (layer 3)
     [ 
        LAYERS,         NUMPAD,     NUMPAD,         NUMPAD,     KC.LCTL(KC.EQUAL),
        NUMPAD,         NUMPAD,     AFFINITY,       NUMPAD,     KC.LCTL(KC.MINUS),
        KC.LCTL(KC.C),  KC.UP,      KC.LCTL(KC.V),  XXXXXXX,    XXXXXXX,
        KC.LEFT,        KC.DOWN,    KC.RIGHT,       NUMPAD,     XXXXXXX,
        NUMPAD,         XXXXXXX,    NUMPAD,         XXXXXXX,    XXXXXXX,
     ],
    # VSCODE (layer 4)
     [ 
        LAYERS,         NUMPAD,     NUMPAD,         NUMPAD,     KC.LCTL(KC.EQUAL),
        KC.LCTL(KC.S),  NUMPAD,     AFFINITY,       NUMPAD,     KC.LCTL(KC.MINUS),
        KC.LCTL(KC.C),  KC.UP,      KC.LCTL(KC.V),  XXXXXXX,    XXXXXXX,
        KC.LEFT,        KC.DOWN,    KC.RIGHT,       KC.LSFT,    XXXXXXX,
        NUMPAD,         XXXXXXX,    NUMPAD,         XXXXXXX,    XXXXXXX,
     ],
    # NAVPAD (layer 5)
     [ 
        LAYERS,     NUMPAD,     NUMPAD,     NUMPAD,     KC.VOLU,
        NUMPAD,     NUMPAD,     AFFINITY,   NUMPAD,     KC.VOLD,
        AFFINITY,   VSCODE,     NUMPAD,     XXXXXXX,    XXXXXXX,
        NUMPAD,     NAVPAD,     ALTPAD,     NUMPAD,     XXXXXXX,
        NUMPAD,     XXXXXXX,    NUMPAD,     XXXXXXX,    XXXXXXX,
     ],
]

if __name__ == '__main__':
    keyboard.go()
