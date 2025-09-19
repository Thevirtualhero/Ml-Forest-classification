import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.title("Forest Cover Type Prediction Using Machine Learning \U0001F333")

# Load model with error handling

def load_model(preferred_paths=("best_knn_model.pkl", "model.pkl")):
    for p in preferred_paths:
        try:
            with open(p, "rb") as f:
                m = pickle.load(f)
            st.info(f"Loaded model from {p}")
            return m
        except FileNotFoundError:
            continue
        except Exception as e:
            st.error(f"Error loading model from {p}: {e}")
            return None
    st.error(f"No model found. Looked for: {preferred_paths}")
    return None


model = load_model()

# Determine feature names to render inputs in the correct order
if model is not None and hasattr(model, 'feature_names_in_'):
    feature_names = list(model.feature_names_in_)
else:
    feature_names = [f"Feature {i+1}" for i in range(15)]

input_vals = []
st.subheader("Enter feature values")
cols = st.columns(3)
for i, name in enumerate(feature_names):
    col = cols[i % 3]
    # show shorter names in the UI if they are long
    label = name if len(name) < 30 else name[:27] + '...'
    val = col.number_input(label, value=0.0, format="%.6f")
    input_vals.append(val)

if st.button("Predict"):
    if model is None:
        st.error("No model loaded. Prediction unavailable.")
    else:
        try:
            n_features = len(input_vals)
            if model is not None and hasattr(model, 'feature_names_in_'):
                cols = list(model.feature_names_in_)
                if len(cols) != n_features:
                    st.warning(f"Model expects {len(cols)} features, but you provided {n_features}.")
                    # Trim or pad the columns to match the provided inputs
                    cols = cols[:n_features]
            else:
                cols = [f"Feature {i+1}" for i in range(n_features)]

            X_df = pd.DataFrame([input_vals], columns=cols)
            # show debug table so we can verify ordering in the server
            st.write("Input DataFrame:")
            st.dataframe(X_df)

            pred = model.predict(X_df)
            st.success(f"Prediction: {pred[0]}")
            # also show raw prediction for debugging
            st.write({"raw_prediction": pred.tolist()})
        except Exception as e:
            st.error(f"Prediction error: {e}")
