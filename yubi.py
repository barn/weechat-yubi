# -*- coding: utf-8 -*-
#
# If you have a yubikey, and you're learning to use it/have coworkers who love
# pressing it, this script will prevent you from pasting it in to IRC at least.
#
# /python load yubi.py
#
# Set the variable for whatever the first few characters of your yubikey string
# may be:
# /set plugins.var.python.yubi.yubistring "vvrnp"
#

import weechat as w

SCRIPT_NAME = "yubi"
SCRIPT_AUTHOR = "Ben Hughes <w@mumble.org.uk>"
SCRIPT_VERSION = "0.2"
SCRIPT_LICENSE = "BSD"
SCRIPT_DESC = "Stops you being yubikeyed"


if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
              SCRIPT_DESC, "", ""):

    # Hooks we want to hook
    hook_command_run = {
        "input": ("/input return",  "command_run_input"),
    }
    # Hook all hooks !
    for hook, value in hook_command_run.iteritems():
        w.hook_command_run(value[0], value[1], "")


def command_run_input(data, buffer, command):
    """ Function called when a command "/input xxxx" is run """
    if command == "/input return":  # As in enter was pressed.

        # Get input contents
        input_s = w.buffer_get_string(buffer, 'input')

        # Skip modification of settings
        if input_s.startswith('/'):
            return w.WEECHAT_RC_OK

        yubistring = w.config_get_plugin('yubistring')

        if yubistring != '':

            # if it's longer than 6 characters, chop it down.
            if len(yubistring) > 6:
                yubistring = yubistring[:6]

            if input_s.startswith(yubistring) and len(input_s) == 44:
                input_s = ''

        # Spit it out
        w.buffer_set(buffer, 'input', input_s)
    return w.WEECHAT_RC_OK
