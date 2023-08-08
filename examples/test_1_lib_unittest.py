#!/usr/bin/env python3

import unittest
from Library import *


class TestLibraryItem(unittest.TestCase):
    """Unit tests for LibraryItem class."""

    def test_init_and_getters(self):
        """Test init and getter methods."""
        item_id, title = '123456', 'Catcher in the Rye'
        item = LibraryItem(item_id, title)

        self.assertIsNotNone(item)
        self.assertIsInstance(item, LibraryItem)

        self.assertEqual(item.get_library_item_id(), item_id)
        self.assertEqual(item.get_title(), title)
        self.assertEqual(item.get_check_out_length(), 28)
        self.assertEqual(item.get_location(), 'ON_SHELF')
        self.assertEqual(item.get_checked_out_by(), None)
        self.assertEqual(item.get_requested_by(), None)
        self.assertEqual(item.get_date_checked_out(), -1)

    def test_setters(self):
        """Test setter methods."""
        item = LibraryItem('123456', 'Catcher in the Rye')
        patron1 = Patron('987654', 'Philip J. Fry')
        patron2 = Patron('111111', 'Dr. Zoidberg')

        item.set_location('CHECKED_OUT')
        item.set_checked_out_by(patron1)
        item.set_requested_by(patron2)
        item.set_date_checked_out(4)

        self.assertEqual(item.get_location(), 'CHECKED_OUT')
        self.assertEqual(item.get_checked_out_by(), patron1)
        self.assertEqual(item.get_requested_by(), patron2)
        self.assertEqual(item.get_date_checked_out(), 4)

    def test_is_overdue(self):
        """Test determination of whether item is overdue."""
        item = LibraryItem('123456', 'Catcher in the Rye')
        item.set_date_checked_out(5)

        self.assertFalse(item.is_overdue(33))
        self.assertTrue(item.is_overdue(34))


class TestLibraryItemSubclasses(unittest.TestCase):
    """Unit tests for LibraryItem subclasses."""

    def setUp(self):
        """Common setup for library item subclass testing."""
        self.book = Book('123456', 'Catcher in the Rye', 'J. D. Salinger')
        self.album = Album('101010', 'Puzzle', 'Dada')
        self.movie = Movie('999999', 'Mad Max: Fury Road', 'George Miller')

    def test_init_and_getters(self):
        """Test init and getter methods."""
        self.assertIsNotNone(self.book)
        self.assertIsNotNone(self.album)
        self.assertIsNotNone(self.movie)
        self.assertIsInstance(self.book, Book)
        self.assertIsInstance(self.album, Album)
        self.assertIsInstance(self.movie, Movie)

        self.assertEqual(self.book.get_author(), 'J. D. Salinger')
        self.assertEqual(self.album.get_artist(), 'Dada')
        self.assertEqual(self.movie.get_director(), 'George Miller')

        self.assertEqual(self.book.get_check_out_length(), 21)
        self.assertEqual(self.album.get_check_out_length(), 14)
        self.assertEqual(self.movie.get_check_out_length(), 7)

    def test_is_overdue(self):
        """Test determination of whether items are overdue."""
        self.book.set_date_checked_out(5)
        self.album.set_date_checked_out(5)
        self.movie.set_date_checked_out(5)

        self.assertFalse(self.book.is_overdue(26))
        self.assertFalse(self.album.is_overdue(19))
        self.assertFalse(self.movie.is_overdue(12))
        self.assertTrue(self.book.is_overdue(27))
        self.assertTrue(self.album.is_overdue(20))
        self.assertTrue(self.movie.is_overdue(13))


class TestPatron(unittest.TestCase):
    """Unit tests for Patron class."""

    def test_init_and_getters(self):
        """Test init and getter methods."""
        patron_id, name = '111111', 'Dr. Zoidberg'
        patron = Patron(patron_id, name)

        self.assertIsNotNone(patron)
        self.assertIsInstance(patron, Patron)

        self.assertEqual(patron.get_patron_id(), patron_id)
        self.assertEqual(patron.get_name(), name)
        self.assertEqual(patron.get_checked_out_items(), {})
        self.assertEqual(patron.get_fine_amount(), 0)

    def test_mutators(self):
        """Test mutator methods."""
        patron = Patron('111111', 'Dr. Zoidberg')
        item = LibraryItem('123456', 'Catcher in the Rye')

        patron.add_library_item(item)
        self.assertIn(item.get_library_item_id(), patron.get_checked_out_items())
        self.assertEqual(len(patron.get_checked_out_items()), 1)

        patron.remove_library_item(item)
        self.assertNotIn(item.get_library_item_id(), patron.get_checked_out_items())
        self.assertEqual(len(patron.get_checked_out_items()), 0)

        patron.amend_fine(5.75)
        self.assertAlmostEqual(patron.get_fine_amount(), 5.75)
        patron.amend_fine(-6.0)
        self.assertAlmostEqual(patron.get_fine_amount(), -0.25)

    def test_get_overdue_items(self):
        """Test getting overdue items."""
        patron = Patron('111111', 'Dr. Zoidberg')
        item1 = LibraryItem('123456', 'Catcher in the Rye')

        item1.set_date_checked_out(5)
        patron.add_library_item(item1)
        self.assertNotIn(item1.get_library_item_id(), patron.get_overdue_items(33))
        self.assertIn(item1.get_library_item_id(), patron.get_overdue_items(34))


class TestLibrary(unittest.TestCase):
    """Unit tests for Library class."""

    def setUp(self):
        """Common setup for testing Library class."""
        self.lib = Library()
        self.i1 = LibraryItem('123456', 'Catcher in the Rye')
        self.i2 = LibraryItem('987654', 'Space Jam')
        self.i3 = LibraryItem('999999', 'Mad Max: Fury Road')
        self.p1 = Patron('111111', 'Dr. Zoidberg')
        self.p2 = Patron('555555', 'Philip J. Fry')
        self.lib.add_library_item(self.i1)
        self.lib.add_library_item(self.i2)
        self.lib.add_library_item(self.i3)
        self.lib.add_patron(self.p1)
        self.lib.add_patron(self.p2)

    def test_init_and_getters(self):
        """Test init and attribute getter methods."""
        lib = Library()

        self.assertIsNotNone(lib)
        self.assertIsInstance(lib, Library)

        self.assertEqual(lib.get_holdings(), {})
        self.assertEqual(lib.get_members(), {})
        self.assertEqual(lib.get_current_date(), 0)

    def test_basic_mutators_and_lookups(self):
        """Test basic mutator methods."""
        self.assertIn(self.i1.get_library_item_id(), self.lib.get_holdings())
        self.assertIn(self.p1.get_patron_id(), self.lib.get_members())

        self.assertEqual(self.lib.lookup_library_item_from_id('123456'), self.i1)
        self.assertEqual(self.lib.lookup_library_item_from_id('000000'), None)
        self.assertEqual(self.lib.lookup_patron_from_id('111111'), self.p1)
        self.assertEqual(self.lib.lookup_patron_from_id('000000'), None)


    def test_check_out_library_item(self):
        """Test checking out library items."""
        checkout_to_non_existent_patron = self.lib.check_out_library_item('000000', self.i1.get_library_item_id())
        self.assertEqual(checkout_to_non_existent_patron, 'patron not found')

        checkout_non_existent_item = self.lib.check_out_library_item(self.p1.get_patron_id(), '000000')
        self.assertEqual(checkout_non_existent_item, 'item not found')

        self.i1.set_checked_out_by(self.p1)
        checkout_already_checked_out_item = self.lib.check_out_library_item(self.p2.get_patron_id(), self.i1.get_library_item_id())
        self.assertEqual(checkout_already_checked_out_item, 'item already checked out')

        self.i2.set_requested_by(self.p2)
        checkout_item_requested_by_another_patron = self.lib.check_out_library_item(self.p1.get_patron_id(), self.i2.get_library_item_id())
        self.assertEqual(checkout_item_requested_by_another_patron, 'item on hold by other patron')

        self.i3.set_requested_by(self.p1)
        checkout_successful = self.lib.check_out_library_item(self.p1.get_patron_id(), self.i3.get_library_item_id())
        self.assertEqual(checkout_successful, 'check out successful')
        self.assertEqual(self.i3.get_requested_by(), None)
        self.assertEqual(self.i3.get_checked_out_by(), self.p1)
        self.assertEqual(self.i3.get_date_checked_out(), self.lib.get_current_date())
        self.assertEqual(self.i3.get_location(), 'CHECKED_OUT')
        self.assertIn(self.i3.get_library_item_id(), self.p1.get_checked_out_items())

    def test_return_library_item(self):
        """Test return library items."""
        return_non_existent_item = self.lib.return_library_item('000000')
        self.assertEqual(return_non_existent_item, 'item not found')

        return_not_checked_out_item = self.lib.return_library_item(self.i1.get_library_item_id())
        self.assertEqual(return_not_checked_out_item, 'item already in library')

        self.lib.check_out_library_item(self.p1.get_patron_id(), self.i1.get_library_item_id())
        self.lib.check_out_library_item(self.p1.get_patron_id(), self.i2.get_library_item_id())
        self.i2.set_requested_by(self.p2)
        return_successful1 = self.lib.return_library_item(self.i1.get_library_item_id())
        return_successful2 = self.lib.return_library_item(self.i2.get_library_item_id())
        self.assertEqual(return_successful1, 'return successful')
        self.assertNotIn(self.i1.get_library_item_id(), self.p1.get_checked_out_items())
        self.assertEqual(self.i1.get_location(), 'ON_SHELF')
        self.assertEqual(self.i2.get_location(), 'ON_HOLD_SHELF')

        self.assertEqual(self.i1.get_checked_out_by(), None)

    def test_request_library_item(self):
        """Test return library items."""
        request_by_non_existent_patron = self.lib.request_library_item('000000', self.i1.get_library_item_id())
        self.assertEqual(request_by_non_existent_patron, 'patron not found')

        request_non_existent_item = self.lib.request_library_item(self.p1.get_patron_id(), '000000')
        self.assertEqual(request_non_existent_item, 'item not found')

        self.i1.set_requested_by(self.p2)
        request_already_requested_item = self.lib.request_library_item(self.p1.get_patron_id(), self.i1.get_library_item_id())
        self.assertEqual(request_already_requested_item, 'item already on hold')

        request_successful = self.lib.request_library_item(self.p1.get_patron_id(), self.i2.get_library_item_id())
        self.assertEqual(request_successful, 'request successful')
        self.assertEqual(self.i2.get_requested_by(), self.p1)
        self.assertEqual(self.i2.get_location(), 'ON_HOLD_SHELF')

    def test_pay_fine(self):
        """Test processing a fine payment."""
        pay_fine_by_non_existent_patron = self.lib.pay_fine('000000', 0.50)
        self.assertEqual(pay_fine_by_non_existent_patron, 'patron not found')

        self.p1.amend_fine(1.50)
        pay_fine_successfully = self.lib.pay_fine(self.p1.get_patron_id(), 1.50)
        self.assertEqual(pay_fine_successfully, 'payment successful')
        self.assertEqual(self.p1.get_fine_amount(), 0)

    def test_increment_current_date(self):
        """Test incrementing the current library date."""
        self.lib.check_out_library_item(self.p1.get_patron_id(), self.i1.get_library_item_id())
        self.lib.check_out_library_item(self.p1.get_patron_id(), self.i2.get_library_item_id())
        for _ in range(28): self.lib.increment_current_date()
        self.assertEqual(self.lib.get_current_date(), 28)
        self.assertAlmostEqual(self.p1.get_fine_amount(), 0)
        self.assertAlmostEqual(self.p2.get_fine_amount(), 0)

        for _ in range(28): self.lib.increment_current_date()
        self.assertEqual(self.lib.get_current_date(), 56)
        self.assertAlmostEqual(self.p1.get_fine_amount(), 5.60)
        self.assertAlmostEqual(self.p2.get_fine_amount(), 0)
