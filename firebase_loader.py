import streamlit as st
import json
from firebase_utils import init_firebase, save_template_to_firebase, load_template_from_firebase, list_all_templates

init_firebase()
