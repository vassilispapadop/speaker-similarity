# routes of website besides auth page
from flask import Blueprint, render_template, request, flash, jsonify
from .process_audio import download_audio, create_segments
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def home():
    segments = []
    if request.method == 'POST':
        url = request.form.get('note')          
        file = download_audio(url)
        print(f'Downloaded file: {file}')
        segments = create_segments(path = file, segment_duration = 5)
        return render_template("segments.html", title = file, segments=segments)
    else:    
        return render_template("home.html")
