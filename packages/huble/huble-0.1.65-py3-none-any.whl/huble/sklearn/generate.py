#from sklearn import metrics
from jinja2 import Environment, FileSystemLoader
#import process.generate as preprocess
#import train.generate as train
from .train import train_generate
from .process import preprocess_generate
from .metrics import log_metrics

from .train.templates import logistic_regression


def generate_file(url,graph,colab=False):

    preprocess_template = preprocess_generate(graph)
    train_template = logistic_regression()
    #output_template = preprocess_template + train_template
    if colab:
        with open("/content/output.py", "w") as f:
            f.write("import huble\n")
            f.write("from sklearn.model_selection import train_test_split\n")
            f.write(f"data=huble.util.load_dataset({url})")
            f.write(preprocess_template)
            f.write("\nX = data.drop(columns = ['PClass'],axis = 1)\n")
            f.write("y = data['PClass']\n")
            f.write("X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n")
            f.write(train_template)
            f.write("\nmodel.fit(X,y)\n")
            f.write("y_pred = model.predict(X_test)\n")
            #metrics template
            f.write("huble.sklearn.metrics.log_metrics(y_test, y_pred,'regression)\n")
    else:
        with open("output.py", "w") as f:
            f.write("import huble\n")
            f.write("from sklearn.model_selection import train_test_split\n")
            f.write(f"data=huble.util.load_dataset({url})")
            f.write(preprocess_template)
            f.write("\nX = data.drop(columns = ['PClass'],axis = 1)\n")
            f.write("y = data['PClass']\n")
            f.write("X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n")
            f.write(train_template)
            f.write("\nmodel.fit(X,y)\n")
            f.write("y_pred = model.predict(X_test)\n")
            #metrics template
            f.write("huble.sklearn.metrics.log_metrics(y_test, y_pred,'regression)\n")
        

    #print(output_template)

