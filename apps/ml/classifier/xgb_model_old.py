import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import FunctionTransformer
import json
import pickle
import xgboost
print(xgboost.__version__)
class MLModel:
    def log_transform(self,x):
        return np.log(x + 1)

    def preprocess(self,df):
        df = df.dropna(0)
        df.drop(columns=['Id'], inplace=True)
        transformer = FunctionTransformer(self.log_transform)
        df['MonthlyIncome']= transformer.transform(df['MonthlyIncome'])
        df['DebtRatio'] =  transformer.transform(df['MonthlyIncome'])
        df['RevolvingUtilizationOfUnsecuredLines'] = transformer.transform(df['RevolvingUtilizationOfUnsecuredLines'])

        X = df.values
        return X
    
    def predict(self,input_data):
        with open ('apps/ml/classifier/xgb.pkl','rb') as f: model = pickle.load(f)
        df = pd.DataFrame(input_data, index=[0])
        X = self.preprocess(df)
        y_pred = model.predict(X)
        y_pred_p = model.predict_proba(X)
        y_pred_p = y_pred_p.squeeze(0)

        if y_pred_p[1] > 0.5:
            label = 1
            prob = y_pred_p[1]
        else:
            label = 0
            prob = y_pred_p[0]

        return {'label':label, 'probability': prob}

"""
if __name__ == '__main__':
    query = {"Id": 123, "RevolvingUtilizationOfUnsecuredLines":0.5687887921,
    "age":45,"NumberOfTime30-59DaysPastDueNotWorse":2,
    "DebtRatio":2.3143490976,"MonthlyIncome":9.1183347262,
    "NumberOfOpenCreditLinesAndLoans":13,
    "NumberOfTimes90DaysLate":0,
    "NumberRealEstateLoansOrLines":6,
    "NumberOfTime60-89DaysPastDueNotWorse":0,
    "NumberOfDependents":2.0}
    XX = MLModel()
    XX.predict(query)
"""
