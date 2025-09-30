#### Written by FSU Automation Team
import base64
import json
from flask import Flask, render_template, request
import requests
import fitz 
from io import BytesIO

app = Flask(__name__)
app.secret_key = "##$$"

@app.route('/')
def index():
    return render_template('Index.html') 

@app.route('/generate-bill', methods=['POST'])
def parlament():
    '''cuz bill maker'''
    if request.method == "POST":
        title = request.form.get('title')
        date = request.form.get('date')
      
        table_values = request.form['table'].split(",")
        table_json = request.form.get('table')  # This is JSON string

        table_values = json.loads(table_json)  
        print(table_values)
        list_of_lists = table_values
        
        total = sum([float(i[5]) for i in list_of_lists])
        print(list_of_lists)

        # image creation
        images_base64 = []  # list of dicts {filename, mime_type, data}
        for key in request.files:
            file = request.files[key]
            file_bytes = file.read()
            encoded_str = base64.b64encode(file_bytes).decode("utf-8")
            mime_type = file.mimetype  
            images_base64.append({
                "filename": file.filename,
                "mime_type": mime_type,
                "data": encoded_str
            })

        url = "https://api.pdfendpoint.com/v1/convert"
        
        rd = render_template(
            'bill-new.html',
            title=title,
            date=date,
            tableData=list_of_lists,
            total=total,
            downloadLink="",
            downloadName="",
            images=images_base64
        )
        
        payload = {
            "html": rd,
            "margin_top": "0cm",
            "margin_bottom": "0cm",
            "margin_right": "0cm",
            "margin_left": "0cm",
            "no_backgrounds": False,
            "no_images":False,
            "printBackground":True,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer pdfe_live_e2386b010bda9ea889d9a1dc16cb9cd41076"
        }
        
        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.json())
     
        aa = (response.json()['data']['url'])

        data_pdf = requests.get(aa)
        doc = fitz.open(stream=data_pdf.content, filetype="pdf")
        page = doc[0]  # first page
        pix = page.get_pixmap(dpi=300)

        img_bytes = pix.tobytes("png")   # raw PNG bytes
        img_io = BytesIO(img_bytes)      # wrap in BytesIO if needed

        encoded_str = base64.b64encode(img_bytes).decode("utf-8")
        images_base64.append({
            "filename": 'firstpage.png',
            "mime_type": 'image/png',
            "data": encoded_str
        })

        return render_template(
            'bill-new.html',
            title=title,
            date=date,
            tableData=list_of_lists,
            total=total,
            downloadLink=aa,
            downloadName="Download? Zoom out if you can't see complete table!.\nScroll Below to see your images and press it to download (your first page picture is also there)",
            images=images_base64
        )
if __name__ == '__main__':
    app.run(debug=True)