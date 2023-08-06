from __future__ import annotations

import reftool
from ttf import Block
from reftool.note import Note


class Item:
    '''
    The Item class represents a catergory of references. It consist of a title and a list of notes for
    that specific catergory.
    '''
    headline_size = None
    headline_color = None

    def __init__(self, title: str, notes: list[Note]) -> None:
        '''
        Creates a new Item object and initializes its title and notes propery.

        Parameters:
            title           Title of the category
            notes           List of Note objects for the category

        Returns:
            None
        '''
        self.title = title
        self.notes = notes

    def initialize(headline_size: int, headline_color: str) -> None:
        '''
        This function initializes static variables which are used inside the Item class.

        Parameters:
            headline_size      Size of the headline blocks
            headline_color     Color of the headline blocks

        Returns:
            None
        '''
        Item.headline_size = headline_size
        Item.headline_color = headline_color

    def print_item(self, count: int = None) -> None:
        '''
        Print the whole Item object. This will print one block row for the headline of the Item
        as well as one block row for each note that is contained inside the item.

        Parameters:
            count           The position of the reference within a list

        Returns:
            None
        '''
        offset_block = Block.createEmptyBlock(reftool.reference.Reference.initial_indent)

        headline_padding = [1, 0, 0, 0]

        if count is not None and count == 0:
            headline_padding[0] = 0

        headline_head = [self.title, Item.headline_color, False]
        headline_body = ['', 'none', 0]
        headline_block = Block(Item.headline_size, headline_padding, headline_head, headline_body)

        offset_block.right = headline_block
        offset_block.buildBlockChain()
        offset_block.printBlockChain()

        for note in self.notes:
            note.print_note()

    def print_items(item_list: list[Item]) -> None:
        '''
        Helper function that can be used to print a list of Items.

        Parameters:
            item_list       List of items to print

        Returns:
            None
        '''
        ctr = 0

        for item in item_list:
            item.print_item(ctr)
            ctr += 1

    def parse_items(items: list[dict]) -> list[Item]:
        '''
        Parses a list of Item objects represented as dictionary objects.

        Parameters:
            items           List of dicitonary objects representing Items

        Returns:
            item_list       List of parsed Item objects
        '''
        item_list = []

        try:

            for item in items:
                notes = Note.parse_notes(item['Notes'])
                new_item = Item(item['Name'], notes)
                item_list.append(new_item)

        except KeyError as e:
            print(f'[-] Error: Found reference without a {e} section.')
            return []

        return item_list

    def get_note(self, number: int) -> Note:
        '''
        Returns the Note object that is related to the number given as argument.

        Parameters:
            number          Number of the note that should be returned

        Returns:
            note            Note object for the specified number
        '''
        for note in self.notes:

            if note.number == number:
                return note

        return None
