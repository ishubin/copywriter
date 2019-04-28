#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import yaml
import os

__config_file__ = '.license-headers.yaml'


def load_config_yaml():
    with open(__config_file__, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print('Could not find ' + __config_file__)


def get_file_extension(file_name):
    return os.path.splitext(file_name)[-1]


def add_license_header(file_path, header_lines, skip_shebang):
    seek_line = 0

    with open(file_path, 'r+') as f:
        first_line = f.readline()

        if skip_shebang and first_line.startswith('#!'):
            seek_line = 1
            first_line = f.readline()

        if first_line != header_lines[0] + '\n':
            print('Adding header to ' + file_path)
            f.seek(seek_line, 0)
            content = f.read()
            f.seek(seek_line, 0)

            for header_line in header_lines:
                f.write(header_line + '\n')
            f.write(content)





if __name__ == '__main__':
    config = load_config_yaml()

    extension_templates = dict()
    for file_type, file_config in config['files'].iteritems():
        for extension in file_config['extensions']:
            skip_shebang = False
            if 'skip_shebang' in file_config:
                skip_shebang = file_config['skip_shebang']

            extension_templates[extension] = dict(
                template_lines=file_config['template'].split('\n'),
                skip_shebang=skip_shebang
            )

    for path in config['paths']:
        for root, dirs, files in os.walk(path):
            for f in files:
                extension = get_file_extension(f)
                if extension in extension_templates:
                    add_license_header(root + '/' + f, extension_templates[extension]['template_lines'], extension_templates[extension]['skip_shebang'])
