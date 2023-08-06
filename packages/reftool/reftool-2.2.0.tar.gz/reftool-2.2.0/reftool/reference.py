from __future__ import annotations

import os
import re
import sys
import yaml

from pathlib import Path
from reftool.note import Note
from reftool.item import Item
from ttf import coloredWrapper


class Reference:
    '''
    A Reference object contains a collection of references regarding a particular topic.
    '''
    reference_path = None
    completer_path = None
    initial_indent = None

    def __init__(self, name: str, items: list[Item]) -> None:
        '''
        Initializes a new Reference object, which consits out of a name and
        a list of Item objects.

        Parameters:
            name                    Name of the reference (name of .yml file)
            items                   List of items inside this reference

        Returns:
            None
        '''
        self.name = name
        self.items = items

    def initialize(reference_path: Path, completer_path: Path, initial_indent: int) -> None:
        '''
        Sets some static attributes that are used by each Reference object.

        Parameters:
            reference_path          Path to the directory there the .yml files are stored
            completer_path          Path to the directory there the completer scripts are stored
            initial_indent          Indent which is used for all printed objects

        Returns:
            None
        '''
        Reference.reference_path = reference_path
        Reference.completer_path = completer_path
        Reference.initial_indent = initial_indent

    def print(self) -> None:
        '''
        Prints formatted output of all items inside this reference.

        Parameters:
            None

        Returns:
            None
        '''
        Item.print_items(self.items)

    def get_references() -> list[Path]:
        '''
        Returns a list of Path objects, one for each reference found within the configured
        reference path.

        Parameters:
            None

        Returns:
            list                    List of Path objects, one for each reference
        '''
        return Reference.reference_path.glob('**/*.yml')

    def list_references(expression: str = '') -> list[str]:
        '''
        Returns a list of all available references that start with the specified expression.
        References are returned as string, not as object.

        Parameters:
            expression              Only references starting with expression are returned

        Returns:
            filtered_references     List of references which start with expression
        '''
        all_references = list(map(lambda x: x.stem, Reference.get_references()))
        filtered_references = list(filter(lambda x: x.startswith(expression), all_references))
        return filtered_references

    def print_references(expression: str) -> None:
        '''
        Prints a list of all available references that start with the specified expression.
        References are returned as string, not as object.

        Parameters:
            expression              Only references starting with expression are printed

        Returns:
            None
        '''
        for reference in Reference.list_references(expression):
            print(reference)

    def search_references(expression: str) -> list[str]:
        '''
        Search the contents of all references for an expression and return a list of strings,
        containing the matching reference names.

        Parameters:
            expression              Expression to look for

        Returns:
            matches                 All references that contain the specified expression
        '''
        matches = []

        try:
            regex = re.compile(expression)

        except re.error:
            print("[-] Error: Invalid regular expression syntax!")
            return []

        for reference in Reference.get_references():

            content = reference.read_text()

            if regex.search(content):
                matches.append(reference.stem)

        return matches

    def pretty_print_list(headline: str, value_list: str) -> None:
        '''
        Helper function to print the returned lists by search_references.

        Parameters:
            headline                String that is used as a headline.
            value_list              List of items that need to be printed.

        Returns:
            None
        '''
        prefix = coloredWrapper('[+] ', Note.text_color)
        headline = coloredWrapper(headline, Item.headline_color)
        values = list(map(lambda x: coloredWrapper(x, Note.count_color), value_list))

        print(f'{prefix}{headline}')

        for value in values:
            print(f'{prefix}  {value}')

    def load_reference(name: str) -> Reference:
        '''
        Creates a new Reference object from a .yml file.

        Parameters:
            name                    Name of the reference that should be loaded.

        Returns:
            Reference               New created reference object.
        '''
        try:
            ref = next(Reference.reference_path.glob(f'**/{name}.yml'))

            with open(ref, "r") as file:
                yaml_data = yaml.safe_load(file)

            item_list = Item.parse_items(yaml_data['Items'])
            return Reference(name, item_list)

        except StopIteration:
            print(f"[-] Error: Cannot find reference with name: {name}")

        except KeyError:
            print(f'[-] Error: Reference {name} does not contain an Items section.')

        return None

    def get_note(self, number):
        '''
        Returns the Note object that is related to the number given as argument.

        Parameters:
            number                  Number of the note that should be returned

        Returns:
            note                    Note object which is related to number
        '''
        for item in self.items:

            note = item.get_note(number)

            if note is not None:
                return note

        print(f'[-] Error: Unable to find note with ID {number} in reference {self.name}')
        return None

    def join_references(reference_list: list[Reference], name: str = 'JoinedRef') -> Reference:
        '''
        Takes a list of reference objects and joins them together into a single reference.

        Parameters:
            reference_list          List of Reference objects
            name                    Name of the joined reference

        Returns:
            joined_ref              Joined Reference object
        '''
        items = []

        for reference in reference_list:

            for item in reference.items:
                item.title = f'[{reference.name}] {item.title}'

            items += reference.items

        joined_ref = Reference(name, items)

        return joined_ref

    def create_matching_reference(expression: str) -> Reference:
        '''
        Finds all references that contain a particular expression and joins them
        together into a single reference.

        Parameters:
            expression              Expression to look for

        Returns:
            joined_ref              Joined Reference object
        '''
        references = Reference.search_references(expression)
        references = list(map(lambda x: Reference.load_reference(x), references))
        joined_ref = Reference.join_references(references)
        return joined_ref

    def filter_reference(self, expression: str) -> None:
        '''
        Removes all Notes from a reference object, that do not match the specified
        expression.

        Parameters:
            expression              Expression to exclude

        Returns:
            None
        '''
        try:
            regex = re.compile(expression)

        except re.error:
            print("[-] Error: Invalid regular expression syntax!")
            return

        items = []
        counter = 1

        for item in self.items:

            notes = []
            for note in item.notes:

                if regex.search(note.text):
                    note.number = str(counter)
                    notes.append(note)
                    counter += 1

            if notes:
                item.notes = notes
                items.append(item)

        self.items = items
