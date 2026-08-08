from matplotlib import cm
import pandas as pd
import json

from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, confusion_matrix)

df=pd.read_csv("evaluation_data.csv")
print("Dataset")
print(df)
print("Missing Values")
print(df.isnull().sum())
print("Data Types")
print(df.dtypes)

df=df.dropna(subset=['label'])

df['label']=df['label'].astype(int)


threshold=0.70
df['prediction']=(df["similarity"]>=threshold).astype(int)

from sklearn.metrics import(
    accuracy_score,precision_score,recall_score,f1_score,confusion_matrix)

y_true=df['label']
y_pred=df['prediction']

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, zero_division=0)
recall = recall_score(y_true, y_pred, zero_division=0)
f1 = f1_score(y_true, y_pred, zero_division=0)
# cm = confusion_matrix(y_true, y_pred)

results = {
    "threshold": threshold,
    "accuracy": round(float(accuracy), 4),
    "precision": round(float(precision), 4),
    "recall": round(float(recall), 4),
    "f1_score": round(float(f1), 4)
}


with open("results.json", "w") as file:
    json.dump(results, file, indent=4)