# Flask Notes Web App

## Overview
This is Project 2 for the 487W Software Engineering course. The Flask Notes Web App is a Flask-based web application designed for managing notes. Users can add, edit, and delete notes. Each note can also have an associated image. The application boasts a user-friendly interface with a search bar to quickly find notes by title, content, or ID. Styling for the web application is provided via CSS, and the database and image storage are managed through Firebase's Firestore and Storage Bucket, respectively.

## File Structure
- `main.py`: This is the primary Python file containing the Flask routes and logic for the application. It manages the interaction between the front-end and the Firebase Firestore database, along with the Storage Bucket.
- `styles.css`: Contains the CSS stylings for the web application.
- `index.html`: The main HTML template for the application, providing the structure and layout of the web page.

## Features
- **Add Note**: Allows users to add new notes with an optional image attachment.
- **Edit Note**: Facilitates the editing of existing notes.
- **Delete Note**: Grants users the ability to remove notes.
- **Search**: Incorporates a search bar, enabling users to efficiently locate notes by title, content, or ID.
- **Sort**: Permits the sorting of notes by name or ID.

## References & Dependencies
- Flask: [Documentation](https://flask.palletsprojects.com/en/2.1.x/)
- Firebase Admin SDK: [Documentation](https://firebase.google.com/docs/admin/setup)
- Jinja2 Template Designer: [Documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/)
- Flask-WTF: [Documentation](https://flask-wtf.readthedocs.io/en/stable/)
- Bootstrap: [CDN Link](https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css)
  
## Author
- Bardan Phuyel
- E-mail: bvp5359@psu.edu

## Video
Watch the [video demonstration](https://youtu.be/GADEJ4An8iU) of the Flask Notes Web App.

## Setup
1. Clone the repository to your local machine.
2. Install the necessary packages using pip.
3. Replace the placeholders in `main.py` with your Firebase credentials.
4. Run the Flask app.

**Note**: Ensure you possess the required Firebase credentials and access to Firestore and Storage Bucket for the application to operate properly.
