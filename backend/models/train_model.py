import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

data = {
    "cgpa": [9.2, 8.8, 8.0, 7.5, 7.0, 6.5],
    "projects": [5, 4, 3, 2, 2, 1],
    "dsa": [1, 1, 1, 0, 0, 0],
    "internship": [1, 1, 0, 0, 0, 0],
    "score": [95, 88, 80, 65, 55, 40]
}

df = pd.DataFrame(data)

X = df[["cgpa", "projects", "dsa", "internship"]]
y = df["score"]

model = RandomForestRegressor()

model.fit(X, y)

joblib.dump(
    model,
    "models/placement_model.pkl"
)

print("Model trained successfully")