import pymongo

from blog.models import Result
import pandas as pd
import numpy as np


def db_process(y_test, y_pred_rgr, y_pred_bst, y_pred_rnn):

    df = pd.DataFrame({
        'Real_result': y_test.reshape(-1),
        'PL_regression': y_pred_rgr.reshape(-1),
        'Gradient_boosting': y_pred_bst,
        'RNN': y_pred_rnn
    })

    df['id'] = np.arange(len(df))+1

    Result.objects.all().delete()

    client = pymongo.MongoClient('mongodb://mongo1:27017')
    db = client["django"]
    collection = db['blog_result']

    df.reset_index(inplace=True)
    df_dict = df.to_dict("records")
    # Insert collection
    collection.insert_many(df_dict)

