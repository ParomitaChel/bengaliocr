from email import message
import os

from flask import Flask, render_template, request, send_file

from ocr import ocr_core,result_ocr,SerachString,ardument_pass, pdf_to_text_ben,word_frequency_with_search

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'jfif', 'pdf'])

global extracted_text
global file_n_1
file_n_1=""
extracted_text=""

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home_page():
    
    return render_template('index.html')


@app.route('/index')
def bengali_ocr():
    
    return render_template('index.html')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/download')
def download():
    return send_file('data/image_result.txt', as_attachment=True)


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    global extracted_text

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            global file_n_1
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            file_n_1= file.filename
            # call the OCR function on it
            extracted_text = ocr_core(file)
            temp = ardument_pass()

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename,message1=ardument_pass())

    elif request.method == 'GET':
        return render_template('upload.html')



@app.route("/search", methods=['POST'])
    
def find_word():
        #Moving forward code
     global file_n_1
     global extracted_text
     forward_message = "Moving Forward..."

     #print(request.form['fname'] + extracted_text )
    # forward_message,extracted_text_search=SerachString(extracted_text,str(request.form['fname']).strip())

     forward_message=SerachString(extracted_text,str(request.form['fname']).strip())
     #return render_template('upload.html',msg='Successfully processed',
     #                              extracted_text=extracted_text_search,
     #                              img_src=UPLOAD_FOLDER + file_n_1,message1=ardument_pass(), forward_message=forward_message)

     word_frequency_search1=word_frequency_with_search(extracted_text,str(request.form['fname']).strip() )
     return render_template('upload.html',msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file_n_1,message1=ardument_pass(), forward_message=forward_message,frequency_text_with_search=word_frequency_search1)


if __name__ == '__main__':
    app.run(debug=True)
