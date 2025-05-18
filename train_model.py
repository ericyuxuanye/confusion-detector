from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import pickle

confused_vals = np.loadtxt("data_c.csv", delimiter=",")
non_confused_vals = np.loadtxt("data_n.csv", delimiter=",")

x = np.concatenate((confused_vals, non_confused_vals))
y = np.zeros(len(confused_vals) + len(non_confused_vals))
y[:len(confused_vals)] = 1

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = SVC(probability=True)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(y_pred)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# save the model
with open("svc_model.pkl", "wb") as f:
    pickle.dump(model, f)
