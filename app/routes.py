from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
import os
from .utils import is_allowed_file
from .config import Config
from werkzeug.utils import secure_filename
import uuid
from app import my_image_classifier


classifier = Blueprint("classifier", __name__)


@classifier.route("/", methods=["GET", "POST"])
def home():
    all_files = os.listdir(Config.UPLOAD_FOLDER)
    full_path_files = ["app/static/" + file for file in all_files]
    all_files = sorted(full_path_files, key=os.path.getctime, reverse=True)

    associated_number = [my_image_classifier.classify_image(file, my_image_classifier.normalize_binary)
                         for file in all_files]

    all_files = [file.replace("app/static/", "") for file in all_files]

    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part", "danger")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No file was selected", "danger")
            return redirect(request.url)
        if file and is_allowed_file(file.filename):
            unique_filename = str(uuid.uuid1())[:5] + ".jpg"
            unique_filename = secure_filename(unique_filename)
            file.save(os.path.join(Config.UPLOAD_FOLDER, unique_filename))

            if len(all_files) + 1 > 6:
                oldest_file = min(full_path_files, key=os.path.getctime)
                os.remove(oldest_file)
        else:
            flash("This format is not supported", "danger")

        return redirect(url_for('classifier.home'))

    return render_template("home.html", title="Home", files=all_files, numbers=associated_number)



