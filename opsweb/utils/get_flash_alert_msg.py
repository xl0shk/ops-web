from flask import get_flashed_messages


def get_flash_alert_message(key):
    flash_alert = get_flashed_messages('alert')
    for msg in flash_alert:
        if msg[0] == key:
            return msg[1]
    return ''
