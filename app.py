from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from main import PersonalAccessSystem

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this in production
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the system
system = PersonalAccessSystem()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Dosya seçilmedi.')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('Dosya seçilmedi.')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the image
            try:
                # Use the system to recognize
                info = system.recognize_face(file_path)
                
                if info:
                    if "Error" in info:
                        flash(f"Hata: {info['Error']}", "error")
                        return render_template('index.html', uploaded_image=filename)
                    else:
                        return render_template('result.html', info=info, uploaded_image=filename)
                else:
                    flash("Yüz eşleşmesi bulunamadı veya veritabanında kayıtlı değil.", "warning")
                    return render_template('index.html', uploaded_image=filename)
                    
            except Exception as e:
                flash(f"Bir hata oluştu: {str(e)}", "error")
                return redirect(request.url)
                
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
