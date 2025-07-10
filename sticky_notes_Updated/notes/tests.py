from django.test import TestCase
from django.urls import reverse
from .models import Note

class NoteViewTests(TestCase):
    """
    Test suite for the views of the 'notes' app.
    It covers all CRUD (Create, Read, Update, Delete) operations.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        This is run once for the entire class.
        """
        cls.note = Note.objects.create(
            title="Test Note 1",
            content="This is the content for the first test note."
        )

    def test_note_list_view(self):
        """
        Test Case: Read all notes (List View).
        Ensures the main page lists all created notes.
        """
        print("Running: test_note_list_view")
        url = reverse('notes:note_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertContains(response, self.note.title)
        print("OK: test_note_list_view")


    def test_note_detail_view(self):
        """
        Test Case: Read a single note (Detail View).
        Ensures a single note's detail page is displayed correctly.
        """
        print("Running: test_note_detail_view")
        url = reverse('notes:note_detail', args=[self.note.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_detail.html')
        self.assertContains(response, self.note.title)
        self.assertContains(response, self.note.content)
        print("OK: test_note_detail_view")

    def test_note_detail_view_not_found(self):
        """
        Test Case: Read a non-existent note.
        Ensures that trying to view a note that doesn't exist returns a 404 Not Found error.
        """
        print("Running: test_note_detail_view_not_found")
        url = reverse('notes:note_detail', args=[999]) # An ID that does not exist
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        print("OK: test_note_detail_view_not_found")


    def test_note_create_view(self):
        """
        Test Case: Create a new note.
        Ensures a new note can be created via a POST request and redirects correctly.
        """
        print("Running: test_note_create_view")
        url = reverse('notes:note_create')
        note_data = {
            'title': 'New Note Title',
            'content': 'Content for the new note.'
        }
        response = self.client.post(url, note_data)

        # Should redirect to the note list page after creation
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes:note_list'))

        # Verify the new note was actually created in the database
        self.assertTrue(Note.objects.filter(title='New Note Title').exists())
        print("OK: test_note_create_view")


    def test_note_update_view(self):
        """
        Test Case: Update an existing note.
        Ensures a note's details can be updated and redirects correctly.
        """
        print("Running: test_note_update_view")
        url = reverse('notes:note_update', args=[self.note.id])
        updated_data = {
            'title': 'Updated Title',
            'content': 'Updated content.'
        }
        response = self.client.post(url, updated_data)

        # Should redirect to the list page after updating
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes:note_list'))

        # Refresh the object from the database to get the updated values
        self.note.refresh_from_db()

        # Verify the note's data was updated
        self.assertEqual(self.note.title, 'Updated Title')
        self.assertEqual(self.note.content, 'Updated content.')
        print("OK: test_note_update_view")


    def test_note_delete_view(self):
        """
        Test Case: Delete an existing note.
        Ensures a note can be deleted and redirects correctly.
        """
        print("Running: test_note_delete_view")
        # Create a new note specifically for this test to avoid conflicts
        note_to_delete = Note.objects.create(title="To Be Deleted", content="Delete me.")
        url = reverse('notes:note_delete', args=[note_to_delete.id])
        response = self.client.post(url)

        # Should redirect to the list page after deletion
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes:note_list'))

        # Verify the note was actually deleted from the database
        self.assertFalse(Note.objects.filter(id=note_to_delete.id).exists())
        print("OK: test_note_delete_view")

