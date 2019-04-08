from keras.models import model_from_json
import sys, os, re, csv, codecs, numpy as np, pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model
from keras import backend as K
from flask import Flask, request
app = Flask(__name__)

tokenizer = Tokenizer(num_words=None,
                      filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                      lower=True,
                      split=" ",
                      char_level=False)

toxicWordsTrain = pd.read_csv("train.csv")
x_train = toxicWordsTrain["comment_text"]
tokenizer.fit_on_texts(list(x_train))


@app.route('/', methods=['GET', 'POST'])
def toxicity_level():

    name= str(request.data)
    name=name[5:]
    print name
    string=str(name)

    # Process string
    new_string = [string]
    new_string = tokenizer.texts_to_sequences(new_string)
    new_string = pad_sequences(new_string, maxlen=371, padding='post', truncating='post')
    
    json_file = open('modeln.json', 'r')

    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("modeln.h5")
    print("Loaded model from disk")
    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])
    # Predict
    prediction = loaded_model.predict(new_string)
    

    # Print output
    print np.argmax(prediction)
    max= np.max(prediction)
    arg=np.argmax(prediction)

    print("Toxicity levels for '{}':".format(string))
    print('Toxic:         {:.0%}'.format(prediction[0][0]))
    print('Severe Toxic:  {:.0%}'.format(prediction[0][1]))
    print('Obscene:       {:.0%}'.format(prediction[0][2]))
    print('Threat:        {:.0%}'.format(prediction[0][3]))
    print('Insult:        {:.0%}'.format(prediction[0][4]))
    print('Identity Hate: {:.0%}'.format(prediction[0][5]))

    k=" "
    if max>0.6:

        switcher = { 
            0: "Toxic", 
            1: "Severe Toxic", 
            2: "Obscene", 
            3: "Threat", 
            4: "Insult", 
            5: "Identity hate", 
        }
    k=switcher.get(arg, " ")
    print k


    K.clear_session()


    return str(k)




#toxicity_level('your face looks like a potato')
#toxicity_level('i will kill you')
#toxicity_level('have a nice day')






if __name__ == '__main__':
      app.run(host='localhost', port=80)
