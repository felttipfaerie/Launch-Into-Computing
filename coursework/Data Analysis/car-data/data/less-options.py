import os
import pandas as pd

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier


# Load dataset
data_path = os.path.join(os.path.dirname(__file__), "car.data")
df = pd.read_csv(data_path, header=None)

columns = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "class"]
df.columns = columns


# Encode categorical values
for col in df.columns:
    df[col] = LabelEncoder().fit_transform(df[col])


# Input feature = class only
X = df[["class"]]


# Spreadsheet output
output_path = os.path.join(os.path.dirname(__file__), "predict_from_class.xlsx")

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

    for target in columns:

        if target == "class":
            continue  # skip predicting class from itself

        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)

        report = classification_report(y_test, y_pred, output_dict=True)

        accuracy_df = pd.DataFrame({"Accuracy": [accuracy]})
        cm_df = pd.DataFrame(cm)
        report_df = pd.DataFrame(report).transpose()

        # Write to sheet
        accuracy_df.to_excel(writer, sheet_name=target, startrow=0, index=False)
        cm_df.to_excel(writer, sheet_name=target, startrow=3)
        report_df.to_excel(writer, sheet_name=target, startrow=10)


print("Spreadsheet created:", output_path)