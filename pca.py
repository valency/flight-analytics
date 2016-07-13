import numpy
import pandas
from sklearn.decomposition import PCA

data_file_name = "history-flight-joined-nobom.csv"
predict_column = "ABNORMALSTATE"
pd_data = pandas.read_csv(data_file_name, quotechar='"', sep=',').fillna(0)
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
print(fit_data.shape)
pca = PCA()
print(pca.fit_transform(fit_data).shape)
print(pca.explained_variance_ratio_)
