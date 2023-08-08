#!/usr/bin/env python3

import pytest
from Library import *


class TestLibraryItem:
    """Unit tests for LibraryItem class."""

    def test_init_and_getters(self):
        """Test init and getter methods."""
        item_id, title = '123456', 'Catcher in the Rye'
        item = LibraryItem(item_id, title)

        assert item is not None
        assert isinstance(item, LibraryItem)

        assert item_id == item.get_library_item_id()
        assert title == item.get_title()
        assert 28 == item.get_check_out_length()
        assert 'ON_SHELF' == item.get_location()
        assert None == item.get_checked_out_by()
        assert None == item.get_requested_by()
        assert -1 == item.get_date_checked_out()

    def test_setters(self):
        """Test setter methods."""
        item = LibraryItem('123456', 'Catcher in the Rye')
        patron1 = Patron('987654', 'Philip J. Fry')
        patron2 = Patron('111111', 'Dr. Zoidberg')

        item.set_location('CHECKED_OUT')
        item.set_checked_out_by(patron1)
        item.set_requested_by(patron2)
        item.set_date_checked_out(4)

        assert 'CHECKED_OUT' == item.get_location()
        assert patron1 == item.get_checked_out_by()
        assert patron2 == item.get_requested_by()
        assert 4 == item.get_date_checked_out()

    def test_is_overdue(self):
        """Test determination of whether item is overdue."""
        item = LibraryItem('123456', 'Catcher in the Rye')
        item.set_date_checked_out(5)

        assert not item.is_overdue(33)
        assert item.is_overdue(34)


class TestLibraryItemSubclasses:
    """Unit tests for LibraryItem subclasses."""

    @pytest.fixture
    def setup(self):
        """Common setup for library item subclass testing."""
        book = Book('123456', 'Catcher in the Rye', 'J. D. Salinger')
        album = Album('101010', 'Puzzle', 'Dada')
        movie = Movie('999999', 'Mad Max: Fury Road', 'George Miller')
        return (book, album, movie)

    def test_init_and_getters(self, setup):
        """Test init and getter methods."""
        book, album, movie = setup

        assert book is not None
        assert album is not None
        assert movie is not None
        assert isinstance(book, Book)
        assert isinstance(album, Album)
        assert isinstance(movie, Movie)

        assert 'J. D. Salinger' == book.get_author()
        assert 'Dada' == album.get_artist()
        assert 'George Miller' == movie.get_director()

        assert 21 == book.get_check_out_length()
        assert 14 == album.get_check_out_length()
        assert 7 == movie.get_check_out_length()

    def test_is_overdue(self, setup):
        """Test determination of whether items are overdue."""
        book, album, movie = setup
        book.set_date_checked_out(5)
        album.set_date_checked_out(5)
        movie.set_date_checked_out(5)

        assert not book.is_overdue(26)
        assert not album.is_overdue(19)
        assert not movie.is_overdue(12)
        assert book.is_overdue(27)
        assert album.is_overdue(20)
        assert movie.is_overdue(13)


class TestPatron:
    """Unit tests for Patron class."""

    def test_init_and_getters(self):
        """Test init and getter methods."""
        patron_id, name = '111111', 'Dr. Zoidberg'
        patron = Patron(patron_id, name)

        assert patron is not None
        assert isinstance(patron, Patron)

        assert patron_id == patron.get_patron_id()
        assert name == patron.get_name()
        assert {} == patron.get_checked_out_items()
        assert 0 == patron.get_fine_amount()

    def test_mutators(self):
        """Test mutator methods."""
        patron = Patron('111111', 'Dr. Zoidberg')
        item = LibraryItem('123456', 'Catcher in the Rye')

        patron.add_library_item(item)
        assert item.get_library_item_id() in patron.get_checked_out_items()
        assert 1 == len(patron.get_checked_out_items())

        patron.remove_library_item(item)
        assert item.get_library_item_id() not in patron.get_checked_out_items()
        assert 0 == len(patron.get_checked_out_items())

        patron.amend_fine(5.75)
        assert 5.75 == pytest.approx(patron.get_fine_amount())
        patron.amend_fine(-6.0)
        assert -0.25 == pytest.approx(patron.get_fine_amount())

    def test_get_overdue_items(self):
        """Test getting overdue items."""
        patron = Patron('111111', 'Dr. Zoidberg')
        item1 = LibraryItem('123456', 'Catcher in the Rye')

        item1.set_date_checked_out(5)
        patron.add_library_item(item1)
        assert item1.get_library_item_id() not in patron.get_overdue_items(33)
        assert item1.get_library_item_id() in patron.get_overdue_items(34)


class TestLibrary:
    """Unit tests for Library class."""

    @pytest.fixture
    def setup(self):
        """Common setup for testing Library class."""
        lib = Library()
        i1 = LibraryItem('123456', 'Catcher in the Rye')
        i2 = LibraryItem('987654', 'Space Jam')
        i3 = LibraryItem('999999', 'Mad Max: Fury Road')
        p1 = Patron('111111', 'Dr. Zoidberg')
        p2 = Patron('555555', 'Philip J. Fry')
        lib.add_library_item(i1)
        lib.add_library_item(i2)
        lib.add_library_item(i3)
        lib.add_patron(p1)
        lib.add_patron(p2)
        return (lib, i1, i2, i3, p1, p2)

    def test_init_and_getters(self):
        """Test init and attribute getter methods."""
        lib = Library()

        assert lib is not None
        assert isinstance(lib, Library)

        assert {} == lib.get_holdings()
        assert {} == lib.get_members()
        assert 0 == lib.get_current_date()

    def test_basic_mutators_and_lookups(self, setup):
        """Test basic mutator methods."""
        lib, i1, i2, i3, p1, p2 = setup

        assert i1.get_library_item_id() in lib.get_holdings()
        assert p1.get_patron_id() in lib.get_members()

        assert i1 == lib.lookup_library_item_from_id('123456')
        assert None == lib.lookup_library_item_from_id('000000')
        assert p1 == lib.lookup_patron_from_id('111111')
        assert None == lib.lookup_patron_from_id('000000')


    def test_check_out_library_item(self, setup):
        """Test checking out library items."""
        lib, i1, i2, i3, p1, p2 = setup

        checkout_to_non_existent_patron = lib.check_out_library_item('000000', i1.get_library_item_id())
        assert 'patron not found' == checkout_to_non_existent_patron

        checkout_non_existent_item = lib.check_out_library_item(p1.get_patron_id(), '000000')
        assert 'item not found' == checkout_non_existent_item

        i1.set_checked_out_by(p1)
        checkout_already_checked_out_item = lib.check_out_library_item(p2.get_patron_id(), i1.get_library_item_id())
        assert 'item already checked out' == checkout_already_checked_out_item

        i2.set_requested_by(p2)
        checkout_item_requested_by_another_patron = lib.check_out_library_item(p1.get_patron_id(), i2.get_library_item_id())
        assert 'item on hold by other patron' == checkout_item_requested_by_another_patron

        i3.set_requested_by(p1)
        checkout_successful = lib.check_out_library_item(p1.get_patron_id(), i3.get_library_item_id())
        assert 'check out successful' == checkout_successful
        assert None == i3.get_requested_by()
        assert p1 == i3.get_checked_out_by()
        assert lib.get_current_date() == i3.get_date_checked_out()
        assert 'CHECKED_OUT' == i3.get_location()
        assert i3.get_library_item_id() in p1.get_checked_out_items()

    def test_return_library_item(self, setup):
        """Test return library items."""
        lib, i1, i2, i3, p1, p2 = setup

        return_non_existent_item = lib.return_library_item('000000')
        assert 'item not found' == return_non_existent_item

        return_not_checked_out_item = lib.return_library_item(i1.get_library_item_id())
        assert 'item already in library' == return_not_checked_out_item

        lib.check_out_library_item(p1.get_patron_id(), i1.get_library_item_id())
        lib.check_out_library_item(p1.get_patron_id(), i2.get_library_item_id())
        i2.set_requested_by(p2)
        return_successful1 = lib.return_library_item(i1.get_library_item_id())
        return_successful2 = lib.return_library_item(i2.get_library_item_id())
        assert 'return successful' == return_successful1
        assert i1.get_library_item_id() not in p1.get_checked_out_items()
        assert 'ON_SHELF' == i1.get_location()
        assert 'ON_HOLD_SHELF' == i2.get_location()

        assert None == i1.get_checked_out_by()

    def test_request_library_item(self, setup):
        """Test return library items."""
        lib, i1, i2, i3, p1, p2 = setup

        request_by_non_existent_patron = lib.request_library_item('000000', i1.get_library_item_id())
        assert 'patron not found' == request_by_non_existent_patron

        request_non_existent_item = lib.request_library_item(p1.get_patron_id(), '000000')
        assert 'item not found' == request_non_existent_item

        i1.set_requested_by(p2)
        request_already_requested_item = lib.request_library_item(p1.get_patron_id(), i1.get_library_item_id())
        assert 'item already on hold' == request_already_requested_item

        request_successful = lib.request_library_item(p1.get_patron_id(), i2.get_library_item_id())
        assert 'request successful' == request_successful
        assert p1 == i2.get_requested_by()
        assert 'ON_HOLD_SHELF' == i2.get_location()

    def test_pay_fine(self, setup):
        """Test processing a fine payment."""
        lib, i1, i2, i3, p1, p2 = setup

        pay_fine_by_non_existent_patron = lib.pay_fine('000000', 0.50)
        assert 'patron not found' == pay_fine_by_non_existent_patron

        p1.amend_fine(1.50)
        pay_fine_successfully = lib.pay_fine(p1.get_patron_id(), 1.50)
        assert 'payment successful' == pay_fine_successfully
        assert 0 == p1.get_fine_amount()

    def test_increment_current_date(self, setup):
        """Test incrementing the current library date."""
        lib, i1, i2, i3, p1, p2 = setup

        lib.check_out_library_item(p1.get_patron_id(), i1.get_library_item_id())
        lib.check_out_library_item(p1.get_patron_id(), i2.get_library_item_id())
        for _ in range(28): lib.increment_current_date()
        assert 28 == lib.get_current_date()
        assert 0 == pytest.approx(p1.get_fine_amount())
        assert 0 == pytest.approx(p2.get_fine_amount())

        for _ in range(28): lib.increment_current_date()
        assert 56 == lib.get_current_date()
        assert 5.60 == pytest.approx(p1.get_fine_amount())
        assert 0 == pytest.approx(p2.get_fine_amount())
