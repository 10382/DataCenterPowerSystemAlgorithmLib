import sys
import json
import redis
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

metrics = ["cpu.usage", "memory.usage"]

# def train(X, y, model_path="./rf.pkl"):
def rf_train(X, y, model_path="model/rf.pkl"):
    rfr = RandomForestRegressor()
    rfr.fit(X, y)
    with open(model_path, "wb") as f:
        pickle.dump(rfr, f)

# def test(X, model_path="./rf.pkl"):
def rf_test(X, model_path="model/rf.pkl"):
    with open(model_path, "rb") as f:
        rfr = pickle.load(f)
    return rfr.predict(X)
