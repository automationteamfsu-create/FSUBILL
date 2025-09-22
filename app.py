import base64
import json
from flask import Flask,render_template,request,make_response
import requests
# from weasyprint import HTML

app = Flask(__name__)
app.secret_key = "##$$"

@app.route('/')
def index():
    return render_template('Index.html') 

@app.route('/generate-bill',methods=['POST'])
def parlament():
    '''cuz bill maker'''
    if request.method == "POST":
        title = request.form.get('title')
        date = request.form.get('date')
      
        table_values = request.form['table'].split(",")
        table_json = request.form.get('table')  # This is JSON string

        table_values = json.loads(table_json)  
        print(table_values)
        list_of_lists =table_values
        
        
        total = sum([float(i[3]) for i in list_of_lists])
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
        print(images_base64)

        
        # rd = 
        # pdf = HTML(string=rd).write_pdf()
        # response=  make_response(pdf)
        # response.headers['Content-Type'] = 'application/pdf'
        # response.headers['Content-Disposition'] = 'inline; filename=page.pdf'
        url = "https://api.pdfendpoint.com/v1/convert"
        
        rd = render_template('bill-new.html', title=title, date=date, tableData=list_of_lists, total=total, downloadLink="", downloadName="",images=images_base64)
        
        payload = {
            "html": rd,
            "margin_top": "0.5cm",
            "margin_bottom": "0.5cm",
            "margin_right": "0.5cm",
            "margin_left": "0.5cm",
            "no_backgrounds": False
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer pdfe_live_3f5c47f0986702d27263684a8730f65f2630"
        }
        
        response = requests.request("POST", url, json=payload, headers=headers)
        aa = (response.json()['data']['url'])
        
        return render_template('bill-new.html', title=title, date=date, tableData=list_of_lists, total=total, downloadLink=aa, downloadName="Download? Zoom out if you can't see complete tabel ",images=images_base64)






    

app.run(debug=True)