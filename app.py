from flask import Flask,render_template,request,make_response
import requests
# from weasyprint import HTML

app = Flask(__name__)
app.secret_key = "##$$"

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/generate-bill',methods=['POST'])
def parlament():
    '''cuz bill maker'''
    if request.method == "POST":
        title = request.form['title']
        date = request.form['date']
        
        table_values = request.form['table'].split(",")
        print(table_values)
        list_of_lists = []
        temp = []
    
        for i in range(0,len(table_values),4):
            temp.append(table_values[i])
            temp.append(table_values[i+1])
            temp.append(table_values[i+2])
            temp.append(table_values[i+1])
            list_of_lists.append(temp)
            temp=[]
        total = sum([float(i[-2]) for i in list_of_lists])
        print(list_of_lists)

        # rd = 
        # pdf = HTML(string=rd).write_pdf()
        # response=  make_response(pdf)
        # response.headers['Content-Type'] = 'application/pdf'
        # response.headers['Content-Disposition'] = 'inline; filename=page.pdf'
        url = "https://api.pdfendpoint.com/v1/convert"

        rd = render_template('bill-new.html',title=title,date=date,tableData= list_of_lists,total=total,downloadLink="",downloadName="")

        payload = {
     "html": rd,
     "margin_top": "1cm",
     "margin_bottom": "1cm",
     "margin_right": "1cm",
     "margin_left": "1cm",
     "no_backgrounds": False
}
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer pdfe_live_3f5c47f0986702d27263684a8730f65f2630"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        aa = (response.json()['data']['url'])

      
        return render_template('bill-new.html',title=title,date=date,tableData= list_of_lists,total=total,downloadLink=aa,downloadName="Download?")
        





    

app.run(debug=True)