import firebase_admin
from firebase_admin import credentials, db
import os

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_key.json")
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
