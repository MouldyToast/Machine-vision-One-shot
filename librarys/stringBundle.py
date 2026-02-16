#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
if items were added in files in the resources/strings folder,
then regenerate the resources module for PyQt6
"""
import re
import os
import sys
import locale
from librarys.ustr import ustr

from librarys.resources import STRINGS_DIR


class StringBundle:

    __create_key = object()

    def __init__(self, create_key, locale_str):
        assert(create_key == StringBundle.__create_key), "StringBundle must be created using StringBundle.getBundle"
        self.id_to_message = {}
        paths = self.__create_lookup_fallback_list(locale_str)
        for path in paths:
            self.__load_bundle(path)

    @classmethod
    def get_bundle(cls, locale_str=None):
        if locale_str is None:
            try:
                locale_str = locale.getdefaultlocale()[0] if locale.getdefaultlocale() and len(
                    locale.getdefaultlocale()) > 0 else os.getenv('LANG')
            except Exception:
                print('Invalid locale')
                locale_str = 'en'

        return StringBundle(cls.__create_key, locale_str)

    def get_string(self, string_id):
        if string_id not in self.id_to_message:
            import logging
            logging.warning("Missing string id: %s — returning key as fallback", string_id)
            return string_id
        return self.id_to_message[string_id]

    def __create_lookup_fallback_list(self, locale_str):
        result_paths = []
        base_path = os.path.join(STRINGS_DIR, "strings")
        result_paths.append(base_path)
        if locale_str is not None:
            # Don't follow standard BCP47. Simple fallback
            tags = re.split('[^a-zA-Z]', locale_str)
            for tag in tags:
                last_path = result_paths[-1]
                result_paths.append(last_path + '-' + tag)

        return [p + '.properties' for p in result_paths]

    def __load_bundle(self, path):
        PROP_SEPERATOR = '='
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    key_value = line.split(PROP_SEPERATOR)
                    key = key_value[0].strip()
                    value = PROP_SEPERATOR.join(key_value[1:]).strip().strip('"')
                    self.id_to_message[key] = value
