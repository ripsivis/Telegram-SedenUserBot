# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
# Copyright (C) 2020-2021 ripsivis <https://github.com/ripsivis>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os.path import isfile
from time import time

from sedenbot import HELP, TEMP_SETTINGS
from sedenecem.core import (
    download_media_wc,
    edit,
    extract_args,
    get_translation,
    reply_video,
    sedenify,
)


@sedenify(pattern='^.upvideo')
def upload(message):
    args = extract_args(message)

    if len(args) < 1:
        edit(message, f'`{get_translation("uploadMedia")}`')
        return

    posix = time()
    TEMP_SETTINGS[f'upload_{posix}'] = posix

    def progress(current, total):
        if (curr_posix := time()) - TEMP_SETTINGS[f'upload_{posix}'] > 5:
            TEMP_SETTINGS[f'upload_{posix}'] = curr_posix
            edit(
                message,
                get_translation(
                    'updownUpload',
                    ['`', '(½{:.2f})'.format(current * 100 / total), args],
                ),
            )

    if isfile(args):
        try:
            edit(message, get_translation('updownUpload', ['`', '', args]))
            reply_video(message, args, progress=progress)
            edit(message, f'`{get_translation("uploadFinish")}`')
        except Exception as e:
            edit(message, f'`{get_translation("uploadError")}`')
            raise e

        del TEMP_SETTINGS[f'upload_{posix}']
        return

    edit(message, f'`{get_translation("uploadFileError")}`')
    del TEMP_SETTINGS[f'upload_{posix}']


HELP.update({'download': get_translation('uploadInfo')})
