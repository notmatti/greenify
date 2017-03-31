# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2017 Matthias Adamczyk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Greenify input that start with ">".

Requires WeeChat version 0.3.7 or higher.

History:
2017-04-01: Matthias Adamczyk <mail@notmatti.me>
    version 0.1: Initial release

https://github.com/notmatti/greenify
"""
import re

import_ok = True
try:
    import weechat
    from weechat import WEECHAT_RC_OK
except ImportError:
    print("Script must be run under weechat. https://weechat.org")
    import_ok = False

SCRIPT_NAME = "greenify"
SCRIPT_AUTHOR = "Matthias Adamczyk <mail@notmatti.me>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "MIT"
SCRIPT_DESC = "Greenify input that start with \">\""
SCRIPT_COMMAND = SCRIPT_NAME


def greenify_input_cb(data, modifier_name, buffer, input_string):
    """Greenify input that start with ">".

    This callback will greenify every input that start with a ">",
    except for messages that start with "> ", ">.>", ">.<" and ">_<".
    """
    regex = re.compile(">_+<")
    match = regex.match(input_string)

    if (input_string.startswith(">")
            and not input_string.startswith("> ")
            and not input_string.startswith(">.<")
            and not input_string.startswith(">.>")
            and match is None):
        input_string = "\x0303{}".format(input_string)
    return input_string


if (__name__ == '__main__'
        and import_ok
        and weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
                             SCRIPT_DESC, '', '')):
    weechat_version = weechat.info_get("version_number", "") or 0
    if int(weechat_version) >= 0x00030700:
        weechat.hook_modifier("input_text_for_buffer", "greenify_input_cb", "")
    else:
        weechat.prnt("", "{}{} requires WeeChat version 0.3.7 or higher.".format(
            weechat.prefix('error'), SCRIPT_NAME))
