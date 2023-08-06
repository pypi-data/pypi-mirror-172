#from sklearn import metrics
from jinja2 import Environment, FileSystemLoader
#import process.generate as preprocess
#import train.generate as train
from .train import train_generate
from .process import preprocess_generate
from huble.util import load_dataset

from .train.templates import logistic_regression

test = """{"nodes":[{"id":"999","type":"custom","position":{"x":633.4002817498528,"y":186.5000289469027},"data":{"name":"Raw Data","value":"Raw Data","color":"green.400","isInput":true,"parameters":{"Dataset":"Test"},"node_type":"preprocess"},"width":400,"height":76,"selected":false,"positionAbsolute":{"x":633.4002817498528,"y":186.5000289469027},"dragging":false},{"id":"998","type":"custom","position":{"x":634.8003512224192,"y":719.1997645651916},"data":{"name":"Clean Data","value":"Clean Data","color":"pink.400","isOutput":true,"parameters":{"Dataset":"Test"},"node_type":"preprocess"},"width":400,"height":76,"selected":false,"positionAbsolute":{"x":634.8003512224192,"y":719.1997645651916},"dragging":false},{"id":"1","type":"custom","position":{"x":546,"y":341},"data":{"name":"Remove NAN values","value":"Remove NAN values","parameters":{"axis":0,"how":"all","subset":[],"inplace":false},"node_type":"preprocess","color":"yellow.400"},"width":400,"height":76,"selected":false,"positionAbsolute":{"x":546,"y":341},"dragging":false},{"id":"3","type":"custom","position":{"x":554,"y":535},"data":{"name":"Dropping rows or columns","value":"Dropping rows or columns","parameters":{"labels":[{"value":"Sex","label":"Sex"},{"value":"Pclass","label":"Pclass"},{"value":"Parch","label":"Parch"}],"axis":0,"index":[],"columns":[],"inplace":false,"errors":"raise"},"node_type":"preprocess","columnList":{"labels":[[{"value":"Survived","label":"Survived"},{"value":"Sex","label":"Sex"}]],"axis":0,"index":[],"columns":[],"inplace":false,"errors":"raise"},"color":"teal.400"},"width":400,"height":76,"selected":true,"positionAbsolute":{"x":554,"y":535},"dragging":false}],"edges":[{"source":"999","sourceHandle":null,"target":"1","targetHandle":null,"type":"custom","data":{"sourceColor":"green.400","targetColor":"yellow.400"},"id":"reactflow__edge-999-1"},{"source":"1","sourceHandle":null,"target":"2","targetHandle":null,"type":"custom","data":{"sourceColor":"yellow.400","targetColor":"#805AD5"},"id":"reactflow__edge-1-2"},{"source":"2","sourceHandle":null,"target":"998","targetHandle":null,"type":"custom","data":{"sourceColor":"#805AD5","targetColor":"pink.400"},"id":"reactflow__edge-2-998"},{"source":"3","sourceHandle":null,"target":"998","targetHandle":null,"type":"custom","data":{"sourceColor":"teal.400","targetColor":"pink.400"},"id":"reactflow__edge-3-998"},{"source":"1","sourceHandle":null,"target":"3","targetHandle":null,"type":"custom","data":{"sourceColor":"yellow.400","targetColor":"teal.400"},"id":"reactflow__edge-1-3"}]}"""
import json
graph = json.loads(test)



def generate_file(url):
    preprocess_template = preprocess_generate(graph)
    train_template = logistic_regression()
    #output_template = preprocess_template + train_template
    with open("/content/output.py", "w") as f:
        f.write("import huble\n")
        f.write("from sklearn.model_selection import train_test_split\n")
        f.write(f"data=load_dataset({url})")
        f.write(preprocess_template)
        f.write("\nX = data.drop(columns = ['PClass'],axis = 1)\n")
        f.write("y = data['PClass']\n")
        f.write("X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n")
        f.write(train_template)
        f.write("\nmodel.fit(X,y)\n")
        f.write("predictions = model.predict(X_test)\n")
        #metrics template

    #print(output_template)

