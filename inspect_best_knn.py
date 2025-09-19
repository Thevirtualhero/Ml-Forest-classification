import pickle
import numpy as np
import pandas as pd
import inspect

MODEL_PATH = r"E:\Guvi class\Gowtham project\my project\Ml\best_knn_model.pkl"

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

print('Model type:', type(model))

# Show common attributes
for attr in ['feature_names_in_', 'n_features_in_', 'named_steps', 'steps']:
    if hasattr(model, attr):
        print(f"{attr}: {getattr(model, attr)}")

# If it's a pipeline, show inner steps
try:
    if hasattr(model, 'named_steps'):
        print('\nPipeline steps:')
        for name, step in model.named_steps.items():
            print('-', name, ':', type(step))
except Exception as e:
    print('Error reading named_steps:', e)

# The sample features you provided
sample = [2678, 45, 10, 8, 710, 0, 0, 220, 232, 151, 0, 0, 1, 1, 1]
print('\nSample vector:', sample)

# Try predict with numpy array
try:
    pred_np = model.predict([sample])
    print('Prediction with numpy list:', pred_np)
except Exception as e:
    print('Predict with list error:', e)

# If model has feature_names_in_, make DataFrame
if hasattr(model, 'feature_names_in_'):
    cols = list(model.feature_names_in_)
    df = pd.DataFrame([sample], columns=cols)
    try:
        pred_df = model.predict(df)
        print('Prediction with DataFrame:', pred_df)
    except Exception as e:
        print('Predict with DataFrame error:', e)

# If pipeline expects columns via ColumnTransformer, attempt to inspect the transformer
try:
    from sklearn.compose import ColumnTransformer
    def find_column_transformers(estimator):
        res = []
        if isinstance(estimator, ColumnTransformer):
            res.append(estimator)
        if hasattr(estimator, 'named_steps'):
            for s in estimator.named_steps.values():
                res += find_column_transformers(s)
        return res

    cts = find_column_transformers(model)
    if cts:
        print('\nFound ColumnTransformer(s):')
        for ct in cts:
            print(ct)
except Exception as e:
    print('ColumnTransformer inspection error:', e)

print('\nDone')
