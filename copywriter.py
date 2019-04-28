#!/usr/bin/env python

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


def add_license_header(file_path, header_lines):
    with open(file_path, 'r+') as f:
        first_line = f.readline()
        if first_line != header_lines[0] + '\n':
            print('Adding header to ' + file_path)
            f.seek(0, 0)
            content = f.read()
            f.seek(0, 0)
            for header_line in header_lines:
                f.write(header_line + '\n')
            f.write(content)





if __name__ == '__main__':
    config = load_config_yaml()


    extension_templates = dict()
    for file_type, file_config in config['files'].iteritems():
        for extension in file_config['extensions']:
            extension_templates[extension] = file_config['template'].split('\n')


    for path in config['paths']:
        for root, dirs, files in os.walk(path):
            for f in files:
                extension = get_file_extension(f)
                if extension in extension_templates:
                    add_license_header(root + '/' + f, extension_templates[extension])

