DOMAIN = "powuhmate"
EVENT = "powuhmate_event"
UUID_READ = "9cf53570-ddd9-47f3-ba63-09acefc60415"
UUID_LED = "847d189e-86ee-4bd2-966f-800832b1259d"

ACTIONS = {
    0x65: "press",
    0x66: "release",
    0x67: "ccw",
    0x68: "cw",
    0x69: "press_ccw",
    0x70: "press_cw",
    0x72: "hold_1",
    0x73: "hold_2",
    0x74: "hold_3",
    0x75: "hold_4",
    0x76: "hold_5",
    0x77: "hold_6",
}
# the button double-fires press/release; drop a repeat within this many seconds
DEBOUNCE = 1.0


def is_duplicate(code, last_code, elapsed):
    return code in (0x65, 0x66) and code == last_code and elapsed < DEBOUNCE
