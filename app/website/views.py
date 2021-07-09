# routes of website besides auth page
from flask import Blueprint, render_template, request, flash, jsonify
from .youtube_dl import download_audio
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('note')          
        download_audio(url)

    return render_template("home.html")
