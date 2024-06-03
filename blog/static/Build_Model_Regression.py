import pandas as pd
import numpy as np
import pymongo
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle


def read_data(table_name):
    client = pymongo.MongoClient('mongodb://mongo1:27017')
    db = client["django"]
    collection = db[table_name]

    cursor = collection.find()
    data = []

    for document in cursor:
        data.append(document)

    df = pd.DataFrame(data)

    if '_id' in df.columns:
        df.drop('_id', axis=1, inplace=True)
    x = df.drop(columns=["Y"], axis=1)
    y = df["Y"].values.reshape(-1, 1)
    return x, y


def preprocessing(x):
    # Define polynomial degree and create PolynomialFeatures transformer
    degree = 2  # đa thức bậc 2
    polynomial_converter = PolynomialFeatures(degree=degree, include_bias=False)  # khởi tạo mô hình y = ax^2+bx+c

    # Transform input features into polynomial features
    poly_features = polynomial_converter.fit_transform(x)
    return poly_features


def create_model_regression(x, y):
    from sklearn.linear_model import LinearRegression  # import library
    poly_features = preprocessing(x)
    # test
    x_train, x_test, y_train, y_test = train_test_split(poly_features, y, test_size=0.3, random_state=101)
    polymodel = LinearRegression()  # model hồi quy
    polymodel.fit(x_train, y_train)
    y_pred = polymodel.predict(x_test)
    MAE_Poly = round(metrics.mean_absolute_error(y_test, y_pred), 2)
    MSE_Poly = round(metrics.mean_squared_error(y_test, y_pred), 2)
    metrics_rgr_df = [MAE_Poly, MSE_Poly]
    # save model to file
    pickle.dump(polymodel, open('blog/static/polymodel.pkl', 'wb'))
    return metrics_rgr_df


def create_model_boosting(x, y):
    from sklearn.ensemble import GradientBoostingRegressor
    poly_features = preprocessing(x)  # call function to get feature
    x_train, x_test, y_train, y_test = train_test_split(poly_features, y, test_size=0.3, random_state=101)
    # Initialize and fit the Gradient Boosting model
    gb_model = GradientBoostingRegressor()
    gb_model.fit(x_train, y_train)
    # Predict on test data
    y_pred_gb = gb_model.predict(x_test)
    # Calculate metrics for measure performance of algorithm
    MAE_gb = round(metrics.mean_absolute_error(y_test, y_pred_gb), 2)
    MSE_gb = round(metrics.mean_squared_error(y_test, y_pred_gb), 2)

    # Display metrics
    metrics_gb_df = [MAE_gb, MSE_gb]
    # save model to file
    pickle.dump(gb_model, open('blog/static/gb_model.pkl', 'wb'))
    return metrics_gb_df


def create_model_RNN(x, y):
    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import Dense, LSTM
    import h5py
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=101)

    # Define RNN model
    rnn_model = Sequential()
    rnn_model.add(LSTM(120, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    rnn_model.add(LSTM(64, return_sequences=False))
    rnn_model.add(Dense(25))
    rnn_model.add(Dense(1))
    # Compile model
    rnn_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Fit model
    rnn_model.fit(x_train, y_train, epochs=10, batch_size=1)

    # Predict on test data
    y_pred_rnn = rnn_model.predict(x_test).flatten()

    # Calculate metrics
    MAE_rnn = round(metrics.mean_absolute_error(y_test, y_pred_rnn), 2)
    MSE_rnn = round(metrics.mean_squared_error(y_test, y_pred_rnn), 2)
    # Display metrics
    metrics_rnn_df = [MAE_rnn, MSE_rnn]
    # save model to file
    rnn_model.save('blog/static/rnn_model.h5')
    return metrics_rnn_df


def training_rgr():
    table_name = 'blog_datatraining'
    x, y = read_data(table_name)
    metrics_rgr_df = create_model_regression(x, y)
    metrics_gb_df = create_model_boosting(x, y)
    metrics_rnn_df = create_model_RNN(x, y)
    print("Build Model Successfully")
    return metrics_rgr_df, metrics_gb_df, metrics_rnn_df