# PS2 Joy Client

Use PlayStation 2 input accessories that cheap "PS2 to USB" dongles don't recognize by dumping gamepad input into UDP packets.

This relies on a [server](https://github.com/adlerosn/ps2joysrv) to be running in your PS2 console.

## Dependencies (will be installed automatically)

- [keyboard>=0.13.5](https://pypi.org/project/keyboard/)

## Installing

0. Download and install [Python](https://www.python.org/downloads/)
1. On a terminal/command prompt, enter: `python -m pip install ps2joycln`

## Running

On Linux: #`python3 -m ps2joycln` (yes, as root (unfortunately))

On Windows: >`python -m ps2joycln`

## Configuration

It defaults the locating of the configuration file to `~/.config/ps2joycln.ini` (or `%USERPROFILE%\.config\ps2joycln.ini`), on port `1469`, creating if not exists.

The `-c` CLI switch allows to specify another place, which can be used as profiles.

The configuration does not hot-reload. Close the application (`Ctrl+C` or whatever) and reopen to apply changes.

On Linux, it requires running as root.

### osu!mania 4k with dance mat

I personally use the snippet below with [DDR skin](https://osu.ppy.sh/community/forums/topics/845193):

```
[pad2]
dir_up=j
dir_dw=f
dir_lf=d
dir_rg=k
```

Reminder: osu!mania 4k is meant to be played with keyboard. It might be an exhausting experience.
