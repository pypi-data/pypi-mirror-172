#!/usr/bin/python3

import os
import configparser

from pathlib import Path
from reftool.item import Item
from reftool.note import Note
from reftool.reference import Reference


def expand(path: str, prefix: str) -> Path:
    '''
    Prefix relative paths with the specified prefix, but leave
    absoultes as they are.

    Parameters:
        path                Relative or absolute file system path
        prefix              Prefix to use for relative paths

    Returns:
        path                Expanded path
    '''
    tmp = Path(path)

    if tmp.is_absolute():
        return tmp

    return Path(prefix).joinpath(path)


def reftool_init() -> None:
    '''
    Initializes the reftool module by setting configuration options
    which were read in from a .ini file.

    Parameters:
        None

    Returns:
        None
    '''
    user_home = Path.home()
    module_path = Path(__file__).parent
    config_parser = configparser.ConfigParser()

    config = module_path.joinpath('resources/reftool.ini')
    user_config = user_home.joinpath('.config/reftool.ini')

    if user_config.exists():
        config = user_config

    config_parser.read(config)

    reference_config = config_parser["Reference"]
    Reference.initialize(
        expand(reference_config["reference_path"], user_home),
        expand(reference_config["completer_path"], user_home),
        int(reference_config["initial_indent"])
    )

    item_config = config_parser["Item"]
    Item.initialize(
            int(item_config["headline_size"]),
            item_config["headline_color"]
    )

    note_config = config_parser["Note"]
    Note.initialize(
            int(note_config["text_size"]),
            note_config["text_color"],
            note_config["count_color"],
            int(note_config["count_padding"]),
            int(note_config["count_indent"]),
            int(note_config["comment_size"]),
            note_config["comment_color"],
            note_config["parameter_color"]
    )
