def return_function(node):
    if node["data"]["value"] == "Logistic Regression":
        return temp_logistic_regression(node['data']['parameters'])
    elif node["data"]["value"] == "SVM (SVC)":
        return temp_svm_svc(node['data']['parameters'])
    elif node["data"]["value"] == "Gaussian Naive Bayes":
        return temp_gaussian_naive_bayes(node['data']['parameters'])
    elif node["data"]["value"] == "Multinomial Naive Bayes":
        return temp_multinomial_naive_bayes(node['data']['parameters'])
    elif node["data"]["value"] == "Stochastic Gradient Descent Classifier":
        return temp_st_gradient_descent(node['data']['parameters'])
    elif node["data"]["value"] == "KNN":
        return temp_knn(node['data']['parameters'])
    elif node["data"]["value"] == "Decision Tree Classifier":
        return temp_decision_tree(node['data']['parameters'])
    elif node["data"]["value"] == "Random Forest Classifier":
        return temp_random_forest(node['data']['parameters'])
    elif node["data"]["value"] == "Gradient Boosting Classifier":
        return temp_gradient_boosting(node['data']['parameters'])
    elif node["data"]["value"] == "LGBM Classifier":
        return temp_lgbm(node['data']['parameters'])
    elif node["data"]["value"] == "XGBoost Classifier":
        return temp_xgboost(node['data']['parameters'])


def temp_logistic_regression():
#     parameters = {
#         "penalty": params["penalty"],
#         "fit_intercept": params["fit_intercept"],
#         "random_state": params["random_state"],
#         "solver": params["solver"],
#         "max_iter": params["max_iter"],
#         "multi_class": params["multi_class"],
#         "tol": params["tol"],
#     }
    return f"model = huble.sklearn.logistic_regression()"


def temp_svm_svc(params):
    parameters = {
        "C" : params['C'], 
        "kernel" : params['kernel'],
        "probability" : params['probability'],
        "random_state": params["random_state"],
        "max_iter": params["max_iter"],
        "decision_function_shape": params["decision_function_shape"],
        "tol": params["tol"],
    }
    return f"model = huble.sklearn.svm_svc(parameters={parameters})"

def temp_gaussian_naive_bayes(params):
    parameters = {
        "priors" : params['priors'],
        "var_smoothing" : params['var_smoothing'],
    }
    return f"model = huble.sklearn.gaussian_naive_bayes(parameters={parameters})"

def temp_multinomial_naive_bayes(params):
    parameters = {
        "class_prior" : params['class_prior'],
        "alpha" : params['alpha'],
        "fit_prior" : params['fit_prior'],
    }
    return f"model = huble.sklearn.multinomial_naive_bayes(parameters={parameters})"

def temp_st_gradient_descent(params):
    parameters = {
        "loss" : params['loss'], 
        "penalty": params["penalty"],
        "fit_intercept": params["fit_intercept"],
        "alpha" : params['alpha'],
        "max_iter": params["max_iter"],
        "tol": params["tol"],
        "random_state": params["random_state"],
        "shuffle" : params['shuffle'],
        "learning_rate" : params['learning_rate'],
        "initial_learning_rate" : params['initial_learning_rate'],
        "early_stopping" : params['early_stopping'],
        "validation_fraction" : params['validation_fraction'],
    }
    return f"model = huble.sklearn.st_gradient_descent(parameters={parameters})"


def temp_knn(params):
    parameters = {
        "n_neighbors" : params['n_neighbors'], 
        "weights" : params['weights'], 
        "algorithm" : params['algorithm'],
        "metric" : params['metric'],
    }
    return f"model = huble.sklearn.knn(parameters={parameters})"


def temp_decision_tree(params):
    parameters = {
        "criterion" : params['criterion'],
        "splitter" : params['splitter'],
        "max_depth" : params['max_depth'],
        "max_leaf_nodes" : params['max_leaf_nodes'],
        "random_state" : params['random_state'],
    }
    return f"model = huble.sklearn.decision_tree(parameters={parameters})"


def temp_random_forest(params):
    parameters = {
        "criterion" : params['criterion'],
        "n_estimators" : params['n_estimators'],
        "max_depth" : params['max_depth'],
        "max_leaf_nodes" : params['max_leaf_nodes'],
        "random_state" : params['random_state'],
    }
    return f"model = huble.sklearn.random_forest(parameters={parameters})"


def temp_gradient_boosting(params):
    parameters = {
        "criterion" : params['criterion'],
        "n_estimators" : params['n_estimators'],
        "max_depth" : params['max_depth'],
        "max_leaf_nodes" : params['max_leaf_nodes'],
        "random_state" : params['random_state'],
        "loss" : params['loss'],
        "learning_rate" : params['learning_rate'],
        "subsample" : params['subsample'],
        "tol" : params['tol'],
    }
    return f"model = huble.sklearn.gradient_boosting(parameters={parameters})"


def temp_lgbm(params):
    parameters = {
        "boosting_type" : params['boosting_type'],
        "num_leaves" : params['num_leaves'],
        "n_estimators" : params['n_estimators'],
        "max_depth" : params['max_depth'],
        "random_state" : params['random_state'],     
        "learning_rate" : params['learning_rate'],
    }
    return f"model = huble.sklearn.lgbm(parameters={parameters})"


def temp_xgboost(params):
    parameters = {
        "n_estimators" : params['n_estimators'],
        "max_depth" : params['max_depth'],
        "random_state" : params['random_state'],     
        "learning_rate" : params['learning_rate'],
    }
    return f"model = huble.sklearn.xgboost(parameters={parameters})"


