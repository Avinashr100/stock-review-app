import streamlit as st
from firebase_admin import credentials, initialize_app
from streamlit.runtime.secrets import secrets
import firebase_admin

def init_firebase():
    if not firebase_admin._apps:
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
            "client_x509_cert_url": secrets.firebase.client_x509_cert_url
        })
        initialize_app(cred, {
            "databaseURL": "https://stock-review-c05a5-default-rtdb.firebaseio.com/"
        })
