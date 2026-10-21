# powuhmate
BLUETOOTH Griffin Powermate expect script and bash example

You will need gatttool.


Files
-

powermate.sh:
it's what I started with. It's an ugly hack.

powuhmate:
an expect script with LED control added in. It's my first time with expect scripts, so it too is an ugly hack, I guess...
There are two ways to use this. One is to have it exec your actions as desired. The second way is to remove all the exec bits from the file and pipe the output to your own script.

Features
-
 - Fast and responsive
 - Minimum delay when controlling LEDs
 - Filters out duplicate events from that horrible, horrible button
 - Did I mention it's fast?

---

LED behavior comments taken (stolen?!?) from https://github.com/stefansundin/powermate-linux/tree/master/bluetooth

Home Assistant
-
`custom_components/powuhmate` is a Home Assistant integration (no gatttool needed; uses HA's Bluetooth stack, so ESPHome Bluetooth proxies work too).

Install: add this repo as a HACS custom repository, or copy `custom_components/powuhmate` into your HA `config/custom_components/`, then restart. Turn the knob; HA discovers it.

Each knob action fires a `powuhmate_event` with `address` and `action`:
`press`, `release`, `cw`, `ccw`, `press_cw`, `press_ccw`, `hold_1` … `hold_6`.

```yaml
automation:
  - trigger:
      - platform: event
        event_type: powuhmate_event
        event_data: { action: cw }
    action:
      - service: media_player.volume_up
        target: { entity_id: media_player.living_room }
```
