"""
Author: Bardan Phuyel
E-mail: bvp5359@psu.edu
Course: CMPSC 487W
Assignment: Project 2
Due date: 10/18/2023
File: main.py
Purpose: Python application that handles Flask Notes web App
Reference(s):
1. Flask Documentation: https://flask.palletsprojects.com/en/2.1.x/
2. Firebase Admin SDK: https://firebase.google.com/docs/admin/setup
3. Jinja2 Template Designer: https://jinja.palletsprojects.com/en/3.0.x/templates/
4. Flask-WTF: https://flask-wtf.readthedocs.io/en/stable/
5. Python Datetime: https://docs.python.org/3/library/datetime.html
6. Firestore Querying Data: https://firebase.google.com/docs/firestore/query-data/queries
7. Flask Request Object: https://flask.palletsprojects.com/en/2.1.x/api/#incoming-request-data
8. Python String Methods: https://docs.python.org/3/library/stdtypes.html#string-methods
9. Flask URL Building: https://flask.palletsprojects.com/en/2.1.x/quickstart/#url-building
10. Python sys library: https://docs.python.org/3/library/sys.html
11. Flask Mega-Tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
12. https://realpython.com/flask-by-example-part-1-project-setup/
13. https://flask.palletsprojects.com/en/2.1.x/tutorial/views/
"""

import datetime
import random

import firebase_admin
from firebase_admin import credentials, firestore, storage
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Firebase Setup with Databse and Storage
FirbaseKey = credentials.Certificate("[replace with your firebase key]]")
firebase_admin.initialize_app(FirbaseKey, {
    'databaseURL': '[replace with your database url]',
    'storageBucket': '[replace with your storage bucket url]]'
})
FBDatabase = firestore.client()
FBStorageBucket = storage.bucket()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        randomNoteID = str(random.randint(1000, 99999))
        inputImage = request.files.get('image')

        image_url = None
        image_name = None

        # Check if there's an uploaded image
        if inputImage and inputImage.filename != '':
            # Upload the image to the storage bucket
            blob = FBStorageBucket.blob(inputImage.filename)
            blob.upload_from_file(inputImage)
            image_name = inputImage.filename
            image_url = blob.generate_signed_url(datetime.timedelta(seconds=3600), method='GET')

        # Create a dictionary to store the note data
        note_data = {
            'randomNoteID': randomNoteID,
            'title': title,
            'content': content,
            'created_at': created_at,
            'image_url': image_url,
            'image_name': image_name
        }

        # Add the note to the database
        FBDatabase.collection('notes').document(randomNoteID).set(note_data)
        return redirect(url_for('index'))

    # finds out if the user wants to filter the notes by name or id
    FilterWith = request.args.get('FilterWith')

    # filter the notes by name or id
    if FilterWith == 'name':
        notes_ref = FBDatabase.collection('notes').order_by('title').stream()
    elif FilterWith == 'id':
        notes_ref = FBDatabase.collection('notes').stream()
    else:
        notes_ref = FBDatabase.collection('notes').stream()

    # Create a list of notes from the database to sort
    NotesList = [{doc.id: doc.to_dict()} for doc in notes_ref]

    if FilterWith == 'id':
        NotesList.sort(key=lambda x: list(x.keys())[0])
        # refreshes the page with the sorted notes
    return render_template('index.html', notes=NotesList)


@app.route('/edit_note/<note_id>', methods=['POST'])
def edit_note(note_id):
    # Get the note from the database to be used
    notesFromDB = FBDatabase.collection('notes').document(note_id)
    note = notesFromDB.get().to_dict()

    # Check if the note exists in the database
    if not note:
        return redirect(url_for('index'))

    # Get the new data from the form
    new_title = request.form.get('new_title', note.get('title'))
    new_content = request.form.get('new_content', note.get('content'))
    new_input_image = request.files.get('new_image')

    # Create an update dictionary
    update_data = {'title': new_title, 'content': new_content}

    # Handle updating the image if a new image is provided
    if new_input_image:
        new_blob = FBStorageBucket.blob(new_input_image.filename)
        new_blob.upload_from_file(new_input_image)

        # Delete the old image from the storage bucket
        old_image_name = note.get('image_url')
        if old_image_name:
            old_blob = FBStorageBucket.blob(old_image_name)
            old_blob.delete()

        update_data['image_url'] = new_blob.generate_signed_url(
            datetime.timedelta(seconds=3600), method='GET')

    # Update the note data in the Firestore database
    notesFromDB.update(update_data)
    return redirect(url_for('index'))


@app.route('/delete_note/<note_id>', methods=['POST'])
def delete_note(note_id):
    notesFromDB = FBDatabase.collection('notes').document(note_id)
    note = notesFromDB.get().to_dict()

    if note:
        # if the note exists in the database, delete the note and delete the image from the storage bucket
        image_name = note.get('image_name')  # Get the blob name/path
        if image_name:
            blob = FBStorageBucket.blob(image_name)
            blob.delete()
        # delete the note from the database
        notesFromDB.delete()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
