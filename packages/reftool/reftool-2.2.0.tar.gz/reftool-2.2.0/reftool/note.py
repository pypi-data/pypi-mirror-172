from __future__ import annotations

import os
import re
import html
import json
import base64
import reftool
import pyperclip
import subprocess

from ttf import Block
from urllib.parse import quote_plus


class Note:
    '''
    The Note class represents one reference about a particular topic. A Note object justs consist
    out of the reference text, a comment and a number which is used to identify the note.

    Parameters:
        None

    Returns:
        None
    '''
    note_count = 1
    text_size = None
    text_color = None
    count_color = None
    count_padding = None
    count_indent = None
    comment_size = None
    comment_color = None
    parameter_color = None

    highlight = re.compile('<([A-Z0-9]+)>')

    def __init__(self, number: str, text: str, comment: str) -> None:
        '''
        Creates a Note object and initializes its number, text and comment properties

        Parameters:
            number               String representation of the Note-ID
            text                 Reference-text of the note
            comment              Comment for the reference

        Returns:
            note                 New Note object
        '''
        self.text = text
        self.number = number
        self.comment = comment
        self.autocomplete = None
        self.truncate = False
        self.lines = None

        Note.note_count += 1

    def initialize(text_size: int, text_color: str, count_color: str, count_padding: int,
                   count_indent: int, comment_size: int, comment_color: str, parameter_color: str) -> None:
        '''
        Initializes variables which were used inside the Note class

        Parameters:
            text_size                        Size of the text component of a Note
            text_color                       Color of the text component of a Note
            count_color                      Color of the count displayed infront of the text of a Note
            count_padding                    Amount of space between a count and the note text
            count_indent                     Additional indent for the Note count
            comment_size                     Size of the comment component of a Note
            comment_color                    Color of the comment component of a Note
            parameter_color                  Color of parameters which are contained inside Note text

        Returns:
            None
        '''
        Note.text_size = text_size
        Note.text_color = text_color
        Note.count_color = count_color
        Note.count_padding = count_padding + 3
        Note.count_indent = count_indent
        Note.comment_size = comment_size
        Note.comment_color = comment_color
        Note.parameter_color = parameter_color

    def print_note(self) -> None:
        '''
        Just prints one block row which consits of padding + number + text + comment

        Parameters:
            None

        Returns:
            None
        '''
        offset_block = Block.createEmptyBlock(reftool.reference.Reference.initial_indent)
        text = self.reduce()

        text_padding = [0, 0, 0, Note.count_indent]
        text_head = [self.number + ')', Note.count_color, False]
        text_body = [text, Note.text_color, Note.count_padding]
        text_block = Block(Note.text_size, text_padding, text_head, text_body)
        text_block.addKeyword('<[A-Z0-9]+>', Note.parameter_color)

        comment_padding = [0, 0, 0, 5]
        comment_head = ['#', Note.comment_color, False]
        comment_body = [self.comment, Note.comment_color, 2]
        comment_block = Block(Note.comment_size, comment_padding, comment_head, comment_body)

        offset_block.right = text_block
        text_block.right = comment_block
        offset_block.buildBlockChain()
        offset_block.printBlockChain()

    def copy_note(self, arguments: list[str], encoding: str = None) -> None:
        '''
        Copies the text attribute of a Note into the clipboard and replaces all keywords
        by the corresponding matches from the argument array.

        Parameters:
            arguments               List of key=value pairs
            encoding                encoding to apply before copy

        Returns:
            None
        '''
        for argument in arguments:

            key, value = argument.split('=', 1)
            self.text = self.text.replace(f'<{key.upper()}>', value)

        if encoding is not None:
            self.apply_encoding(encoding)

        pyperclip.copy(self.text)

    def apply_encoding(self, encoding: str) -> None:
        '''
        Applies the selected encoding to self.text.

        Parameters:
            encoding            Encoding to apply

        Returns:
            None
        '''
        if encoding == 'url':
            self.text = quote_plus(self.text)

        elif encoding == 'URL':
            data = self.text.encode('utf-8')
            hex_form = data.hex()
            self.text = ''

            for i in range(0, len(hex_form), 2):
                self.text += '%' + hex_form[i:i+2]

        elif encoding == 'hex':
            data = self.text.encode('utf-8')
            self.text = data.hex()

        elif encoding == 'json':
            self.text = json.dumps(self.text)[1:-1]

        elif encoding == 'base64':
            text = base64.b64encode(self.text.encode('utf-8'))
            self.text = text.decode('utf-8')

        elif encoding == 'html':
            self.text = html.escape(self.text)

        elif encoding == 'HTML':
            data = self.text.encode('utf-8')
            hex_form = data.hex()
            self.text = ''

            for i in range(0, len(hex_form), 2):
                self.text += '&#x' + hex_form[i:i+2] + ';'

    def get_args(self) -> list[str]:
        '''
        Performs a regex search for arguments inside the note and returns all found
        matches as a list.

        Parameters:
            None

        Returns:
            matches              List off all attributes found
        '''
        matches = Note.highlight.findall(self.text)
        return matches

    def print_args(self):
        '''
        Prints all arguments that can be found inside the text of the note.

        Parameters:
            None

        Returns:
            None
        '''
        for arg in set(self.get_args()):
            print(arg.lower())

    def get_completion(self, param: str) -> list[str]:
        '''
        Returns a list of possible completions for a certain parameter

        Parameters:
            param               Name of the parameter to complete

        Returns:
            list                List of possible completions
        '''
        default = ['[FILE]']

        if self.autocomplete is None or param not in self.autocomplete:
            return default

        comp = self.autocomplete[param]

        try:

            if comp['type'] == 'list':
                return comp['completer']

            if comp['type'] == 'IP':
                return ['[IP]']

            if comp['type'] == 'script' and comp['completer'].endswith('.sh'):

                completer_path = reftool.reference.Reference.completer_path
                for completer_folder in completer_path.glob('**/completers'):

                    script = completer_folder.joinpath(comp['completer'])
                    if script.is_file() and os.access(script, os.X_OK) and completer_path in script.parents:
                        output = subprocess.check_output([script])
                        output = output.decode('utf-8')
                        output = list(filter(None, output.split('\n')))
                        return output

        except KeyError:
            pass

        return default

    def print_completion(self, param: str) -> None:
        '''
        Prints a list of possible completions for the specified parameter.

        Parameters:
            param              Name of the parameter to complete

        Returns:
            None
        '''
        completions = self.get_completion(param)

        for completion in completions:
            print(completion)

    def parse_notes(notes: list[dict]) -> list[Note]:
        '''
        Parses a list of Note objects from a list of dictionary objects.

        Parameters:
            notes               List of dictionary objects describing Notes

        Returns:
            note_list           List of new created Note objects
        '''
        note_list = []

        for note in notes:

            try:
                new_note = Note(str(Note.note_count), note['Text'], note['Comment'])

                if 'Autocomplete' in note:
                    new_note.autocomplete = note['Autocomplete']

                new_note.truncate = note.get('Truncate', False)
                new_note.lines = note.get('Lines')
                note_list.append(new_note)

            except KeyError:
                continue

        return note_list

    def reduce(self):
        '''
        Reduce the content of the Note to better fit into the display. The
        detailed action depends on the 'Lines' and 'Truncate' parameters within
        the note. When 'Lines' was used, only the specified lines of the note are
        displayed. When 'Truncate' was used, lines that are longer than the screen
        width are truncated.

        Parameters:
            None

        Returns:
            reduced         Note with reduced content
        '''
        truncated = False
        lines = self.text.split('\n')

        if self.lines and len(lines) > 1:
            lines = [lines[index] for index in self.lines]
            truncated = True

        if self.truncate:

            for ctr in range(len(lines)):
                if len(lines[ctr]) >= Note.text_size:
                    lines[ctr] = lines[ctr][0:Note.text_size - 15] + '[...]'
                    truncated = True

        if truncated:
            self.comment = '[Truncated] - ' + self.comment

        return '\n'.join(lines)
