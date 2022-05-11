import numpy as np
import pandas as pd 
import joblib


class MLModel:
    def prediction(self, input_data):
        pipe = joblib.load('apps/ml/classifier/pipe-process.joblib')
        df = pd.DataFrame(input_data, index=[0])
        df.drop(columns=['Id'], inplace=True)
        print(df)
        print(pipe[0].transform(df))
        y_pred = pipe.predict(df)
        y_pred_p = pipe.predict_proba(df)
        y_pred_p = y_pred_p.squeeze(0)
        if y_pred_p[1] > 0.5:
            label = y_pred
            prob = y_pred_p[1]
        else:
            label = y_pred
            prob = y_pred_p[1]         
        return {'label': label, 'prob': prob}

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
    XX.prediction(query)

"""
