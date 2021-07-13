# routes of website besides auth page
from flask import Blueprint, render_template, request, flash, jsonify, send_file
from .process_audio import download_audio, create_segments, predict

import json

PATH_TO_CLIPS = 'downloads/parts/'

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def home():
    segments = []
    if request.method == 'POST':
        url = request.form.get('note')          
        if not url:
            return render_template("home.html")

        file = download_audio(url)
        print(f'Downloaded file: {file}')

        # crops file into 10-seconds chunks
        segments = create_segments(path = file, segment_duration = 10)
        pred_dict = predict(segments)
        
        return render_template("segments.html", title = file.rsplit('/', 1)[-1],  pred_dict=pred_dict)
    else:    
        return render_template("home.html")

@views.route('/listen', methods=['POST'])
def listen():
    data = json.loads(request.data)
    # path = data['source']
    # fileName = data['source'].rsplit('/', 1)[-1]
    
    return send_file(
        PATH_TO_CLIPS+data['source'], 
        mimetype="audio/wav", 
        as_attachment=True, 
        attachment_filename=data['source'])