import os
from flask import Flask, request, redirect, url_for, render_template,jsonify,json
import threading
import pandas as pd

pd.options.display.max_colwidth = 100
app = Flask(__name__)
data = pd.read_csv("new.csv") 

i=0

@app.route("/", methods=['GET', 'POST'])
def index():
    kk=get_text()
    data = json.loads(kk)
    k=data['text']
    print k
    return render_template("layout.html", text=k)

def get_text():
    global i
    #print "i in gettext =" + str(i)
    p=str(data.iloc[i])

    p=p[43:].strip()
    ress=p[:-22].strip()
    x = {"text": ress}
    y = json.dumps(x)
    return y


@app.route('/background_process_test')
def background_process_test():
    global i
    i=i+1
    x=get_text()
    print "i is equal tto" + str(i)
    return x
    



def flask_app(app):
    app.run(port = 5052, debug=True)

def main(app):
    flask_app(app)

if __name__ == "__main__":
    main(app)
