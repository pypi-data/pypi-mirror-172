#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import argparse
import configparser
from io import StringIO
from pathlib import Path
import socket

import keyboard


def cli_args():
    parser = argparse.ArgumentParser('ps2joycln')
    config_file_path = Path.home().joinpath('.config').joinpath('ps2joycln.ini')
    parser.add_argument('-c', '--config', metavar='CFG', action='store',
                        type=Path, default=config_file_path,
                        help='custom path for the configuration file')
    return parser.parse_args()


def handle_config_file(config_file_path: Path) -> configparser.ConfigParser:
    config_file_path.parent.mkdir(parents=True, exist_ok=True)
    if not config_file_path.exists():
        config_file_path.write_bytes(b'')
    cp = configparser.ConfigParser()
    cp.read_string(config_file_path.read_text(encoding='utf-8'))
    if 'network' not in cp:
        cp.add_section('network')
    if 'port' not in cp['network']:
        cp['network']['port'] = '1469'
    if 'pad1' not in cp:
        cp.add_section('pad1')
    if 'pad2' not in cp:
        cp.add_section('pad2')
    ds_keys = ['dir_up',
               'dir_dw',
               'dir_lf',
               'dir_rg',
               'rub_st',
               'rub_sl',
               'tbt_cr',
               'tbt_cc',
               'tbt_sq',
               'tbt_tr',
               'sbt_l1',
               'sbt_r1',
               'sbt_l2',
               'sbt_r2',
               'ana_l3',
               'ana_r3']
    pad_sections = [cp['pad1'], cp['pad2']]
    for pad_section in pad_sections:
        for ds_key in ds_keys:
            if ds_key not in pad_section:
                pad_section[ds_key] = ''
    sio = StringIO()
    cp.write(sio, space_around_delimiters=False)
    if config_file_path.read_text(encoding='utf-8') != sio.getvalue():
        config_file_path.write_text(sio.getvalue(), encoding='utf-8')
        print(f'Written: {config_file_path}')
    return cp


KEYPRESSES = {
    0x0001: 'rub_sl',
    0x0002: 'ana_l3',
    0x0004: 'ana_r3',
    0x0008: 'rub_st',
    0x0010: 'dir_up',
    0x0020: 'dir_rg',
    0x0040: 'dir_dw',
    0x0080: 'dir_lf',
    0x0100: 'sbt_l2',
    0x0200: 'sbt_r2',
    0x0400: 'sbt_l1',
    0x0800: 'sbt_r1',
    0x1000: 'tbt_tr',
    0x2000: 'tbt_cc',
    0x4000: 'tbt_cr',
    0x8000: 'tbt_sq',
}


def main():
    args = cli_args()
    config_file_path = Path(args.config)
    config = handle_config_file(config_file_path)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(('', config['network'].getint('port')))
    pads = [set(), set()]
    while True:
        payload, (ipsrc, prsrc) = sock.recvfrom(1500)
        hexstring = payload.decode(encoding='ascii').strip()
        must_be_2_or_6 = int(hexstring[2:4], 16)
        err_if_zero = int(hexstring[4:6], 16)
        err_if_non_zero = int(hexstring[6:8], 16)
        if must_be_2_or_6 in (2, 6,) and err_if_zero != 0 and err_if_non_zero == 0:
            padnum = int(hexstring[0])
            hex_bitmap_press_le = hexstring[10:14]
            hex_bitmap_press_be = (
                hex_bitmap_press_le[2:4] + hex_bitmap_press_le[0:2])
            bitmap_press = (
                (~int(hex_bitmap_press_be, 16)) & 0xFFFF
            )
            thispadset = pads[padnum-1]
            keypresses = {v for k, v in KEYPRESSES.items() if k & bitmap_press}
            pressed = keypresses - thispadset
            unpressed = thispadset - keypresses
            if (len(pressed) > 0 or len(unpressed) > 0):
                padconfig = config[f'pad{padnum}']
                fire_keyboard_events(
                    padconfig, keypresses-pressed, pressed, unpressed)
                print(f'{padnum}: {keypresses=}, {pressed=}, {unpressed=}')
            pads[padnum-1] = keypresses


def fire_keyboard_events(padconfig,
                         previous_presses,
                         started_pressing,
                         stopped_pressing
                         ):
    for sp in stopped_pressing:
        hotkey = padconfig[sp].strip()
        if len(hotkey) > 0:
            keyboard.release(hotkey)
    for sp in started_pressing:
        hotkey = padconfig[sp].strip()
        if len(hotkey) > 0:
            keyboard.press(hotkey)
    for pp in previous_presses:
        hotkey = padconfig[pp].strip()
        if len(hotkey) > 0 and not keyboard.is_pressed(hotkey):
            keyboard.press(hotkey)


if __name__ == '__main__':
    main()
