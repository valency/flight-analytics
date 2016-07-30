import getopt
import sys

import numpy
import pandas
from sklearn import cross_validation
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from common import *


def main(argv):
    usage = 'predict.py -f <data,e.g.,data.csv> -c <predict-column,e.g.,StartDelay> -s <cross-validation,e.g.,10> -d <decomposition,e.g.,10>'
    data_file_name = "data.csv"
    predict_column = "StartDelay"
    decomposition = 10
    cross_validation_set = 10
    try:
        opts, args = getopt.getopt(argv, "hf:c:s:")
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        elif opt == '-f':
            data_file_name = arg
        elif opt == '-c':
            predict_column = arg
        elif opt == '-s':
            cross_validation_set = int(arg)
        elif opt == '-d':
            decomposition = int(arg)
    log("DATA = " + data_file_name)
    log("PREDICT_COLUMN = " + predict_column)
    log("DECOMPOSITION = " + str(decomposition))
    log("FOLDS = " + str(cross_validation_set))
    log("Loading data...")
    pd_data = pandas.read_csv(data_file_name, quotechar='"', sep=',').fillna(0)
    log("Converting data...")
    predict_data = None
    fit_data = None
    for column in pd_data.columns:
        if pd_data[column].dtype == numpy.object:
            column_data = pandas.Categorical.from_array(pd_data[column]).codes
        else:
            column_data = pd_data[column].values
        if column == predict_column:
            predict_data = column_data
        else:
            if fit_data is None:
                fit_data = column_data[numpy.newaxis].T
            else:
                fit_data = numpy.append(fit_data, column_data[numpy.newaxis].T, 1)
    log("Constructing predictors...")
    classifiers_names = ["Nearest Neighbors", "Linear SVM", "Decision Tree", "Random Forest", "AdaBoost", "Naive Bayes"]
    classifiers = [
        KNeighborsClassifier(3),
        SVC(kernel="linear", C=0.025),
        DecisionTreeClassifier(max_depth=5),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        AdaBoostClassifier(),
        GaussianNB()
    ]
    log("Decomposing...")
    pca = PCA(n_components=decomposition + 1)
    fit_data = pca.fit_transform(fit_data)
    fit_data = fit_data[:, 1:]
    log("Predicting...")
    for name, clf in zip(classifiers_names, classifiers):
        scores = cross_validation.cross_val_score(clf, fit_data, predict_data, cv=cross_validation_set)
        print name, numpy.average(scores)


if __name__ == "__main__":
    main(sys.argv[1:])
