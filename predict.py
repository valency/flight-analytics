import getopt
import sys

import numpy
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Imputer
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def main(argv):
    usage = 'predict.py -f <data,e.g.,data.csv> -c <predict-column,e.g.,ABNORMALSTATE> -s <cross-validation,e.g.,10>'
    data_file_name = "history-flight-joined-nobom.csv"
    predict_column = "ABNORMALSTATE"
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
    data = numpy.genfromtxt(data_file_name, delimiter=',')
    new = Imputer().fit_transform(data).astype(int)
    '''
    fit_row_count = data.shape[0] / 2
    predict_row_count = data.shape[0] - fit_row_count
    ground_truth = data[:, 7]
    fit_ground_truth = ground_truth[:fit_row_count]
    predict_ground_truth = ground_truth[fit_row_count:]
    features = numpy.delete(data, 7, 1)
    fit_data = features[:fit_row_count, :]
    predict_data = features[fit_row_count:, :]
    '''

    fit_row_count = new.shape[0] / 2
    predict_row_count = new.shape[0] - fit_row_count
    ground_truth = new[:, 7]
    fit_ground_truth = ground_truth[:fit_row_count]
    predict_ground_truth = ground_truth[fit_row_count:]
    features = numpy.delete(new, 7, 1)
    fit_data = features[:fit_row_count, :]
    predict_data = features[fit_row_count:, :]

    '''
    names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
             "Random Forest", "AdaBoost", "Naive Bayes", "LDA", "QDA"]
    '''

    names = ["Linear SVM", "RBF SVM", "AdaBoost", "Naive Bayes"]
    classifiers = [
        KNeighborsClassifier(3),
        SVC(kernel="linear", C=0.025),
        SVC(gamma=2, C=1),
        DecisionTreeClassifier(max_depth=5),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        AdaBoostClassifier(),
        GaussianNB()
        # LDA()
        # QDA()
    ]

    for name, clf in zip(names, classifiers):
        scores = cross_validation.cross_val_score(clf, features, ground_truth, cv=5)
        print name, numpy.average(scores)
        clf.fit(fit_data, fit_ground_truth)
        predict_result = clf.predict(predict_data)
        # hits = (predict_result == predict_ground_truth).sum()
        # print name, ":", 100.0 * hits / len(predict_ground_truth), "%"


if __name__ == "__main__":
    main(sys.argv[1:])
