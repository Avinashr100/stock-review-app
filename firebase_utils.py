import firebase_admin
from firebase_admin import credentials, db
import os

def init_firebase():
    if not firebase_admin._apps:
from firebase_admin import credentials
from streamlit.runtime.secrets import secrets

cred = credentials.Certificate({
    "type": secrets.firebase.type,
    "project_id": secrets.firebase.project_id,
    "private_key_id": secrets.firebase.private_key_id,
    "private_key": secrets.firebase.private_key,
    "client_email": secrets.firebase.client_email,
    "client_id": secrets.firebase.client_id,
    "auth_uri": secrets.firebase.auth_uri,
    "token_uri": secrets.firebase.token_uri,
    "auth_provider_x509_cert_url": secrets.firebase.auth_provider_x509_cert_url,
    "client_x509_cert_url": secrets.firebase.client_x509_cert_url,
})

        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://stock-review-c05a5-default-rtdb.firebaseio.com/"
        })

def save_template_to_firebase(stock_name, data):
    ref = db.reference(f"templates/{stock_name}")
    ref.set(data)

def load_template_from_firebase(stock_name):
    ref = db.reference(f"templates/{stock_name}")
    return ref.get()

def list_all_templates():
    ref = db.reference("templates")
    return ref.get() or {}
