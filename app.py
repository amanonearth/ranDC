from ranDC import proc, MLclass, GMMHMM, result
import os
from flask import Flask, flash, request, redirect, render_template
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from threading import Thread
import time

app=Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
global filename
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['pcap'])
thread = Thread()
ALREADY_DONE = False

def hack():
    socketio.emit('newnumber', {'number': "Done"}, namespace='/test')
    time.sleep(10)
    socketio.emit('newnumber', {'number': filename}, namespace='/test')
    
    
def predictions():
    global ALREADY_DONE
    pcap=f"uploads/{filename}"
    df = proc(pcap)
    socketio.emit('newnumber', {'number': "Pre-processing Done {pcap converted to pandas DataFrame}"}, namespace='/test')
    mlpred = MLclass(df)
    socketio.emit('newnumber', {'number': "Machine Learning Prediction is done"}, namespace='/test')
    hmmpred = GMMHMM(df)
    socketio.emit('newnumber', {'number': "GMMHMM Prediction is done"}, namespace='/test')
    hmmresult = result(hmmpred)
    socketio.emit('newnumber', {'number': "GMMHMM Result is ready"}, namespace='/test')
    mlresult = result(mlpred)
    socketio.emit('newnumber', {'number': "ML Result is ready"}, namespace='/test')
    socketio.emit('newnumber', {'number': str(mlresult) + str(hmmresult)}, namespace='/test')
    if mlresult[-2] == hmmresult[-2]:
        details = str(round((hmmresult[0][hmmresult[1]])/(hmmresult[0][1]+hmmresult[0][0])*100,2))+"% " + "of the total traffic was found "+('benign' if hmmresult[1]==0 else 'malicious')
        if hmmresult[-2] == "0":
            msz = f"{filename} is Benign"
        else:
            msz = f"{filename} contains Malware Traffic"
    else:
        details = str(round((hmmresult[0][hmmresult[1]])/(hmmresult[0][1]+hmmresult[0][0])*100,2))+"% " + "of the total traffic was found "+('benign' if hmmresult[1]==0 else 'malicious')
        if hmmresult[-2] == "0":
            msz = f"{filename} is Benign"
        else:
            msz = f"{filename} contains Malware Traffic"
    socketio.emit('result', {'number': msz}, namespace='/test')
    socketio.emit('result', {'number': f'Traffic Details: {details}'}, namespace='/test')
    ALREADY_DONE = True
    return hmmresult, mlresult, ALREADY_DONE


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    global filename
    global ALREADY_DONE
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file chosen')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            ALREADY_DONE = False
            return redirect('/')
        else:
            flash('Allowed file types are: pcap')
            return redirect(request.url)


@socketio.on('connect', namespace='/test')
def test_connect():
    global ALREADY_DONE
    global thread
    print('Client connected')
    if not ALREADY_DONE:
        thread = socketio.start_background_task(predictions)
        

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)