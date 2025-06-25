import firebase_admin
from firebase_admin import credentials, db, auth
import requests

# Path to your Firebase service account key JSON file
cred = credentials.Certificate('path/to/serviceAccountKey.json')

# Initialize the Firebase app with database URL
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project-id.firebaseio.com'
})

# Example: Authenticate a user with email and password (requires Firebase REST API)

def sign_in_with_email_and_password(api_key, email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    return response.json()

# Example usage:
api_key = 'YOUR_FIREBASE_WEB_API_KEY'
email = 'user@example.com'
password = 'user_password'
user = sign_in_with_email_and_password(api_key, email, password)
id_token = user.get('idToken')

# Example: Read from the database
ref = db.reference('some/data/path')
data = ref.get()
print(data)

# Example: Write to the database
ref.set({'key': 'value'})