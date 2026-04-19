import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier


# ==========================================
# SETTINGS
# ==========================================

file_path = r"C:\Users\elmak\Documents\Launch Into Computing\coursework\annual income\adult.data"

target_column = "race"

columns = [
    "age","workclass","fnlwgt","education","education_num",
    "marital_status","occupation","relationship","race","sex",
    "capital_gain","capital_loss","hours_per_week","native_country","income"
]

output_folder = r"C:\Users\elmak\Documents\Launch Into Computing\coursework\annual income"


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    file_path,
    names=columns,
    na_values="?",
    skipinitialspace=True
)

print("\nRAW DATA")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ==========================================
# BASIC CLEANING
# ==========================================

df = df.dropna()

print("\nAFTER CLEANING")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ==========================================
# PREPARE FEATURES
# ==========================================

feature_columns = [col for col in df.columns if col != target_column]

model_df = df.copy()
encoders = {}

for col in feature_columns:

    if pd.api.types.is_numeric_dtype(model_df[col]):
        model_df[col] = model_df[col].fillna(model_df[col].median())

    else:
        model_df[col] = model_df[col].fillna("MISSING")
        le = LabelEncoder()
        model_df[col] = le.fit_transform(model_df[col].astype(str))
        encoders[col] = le


# encode target
target_encoder = LabelEncoder()
model_df[target_column] = target_encoder.fit_transform(model_df[target_column])

X = model_df[feature_columns]
y = model_df[target_column]


# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTRAIN / TEST SPLIT")
print("Training rows:", len(X_train))
print("Testing rows :", len(X_test))


# ==========================================
# TRAIN MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)


# ==========================================
# MODEL RESULTS
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\nMODEL RESULTS")
print("Accuracy:", round(accuracy, 4))

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# ==========================================
# CONFUSION MATRIX (NORMALIZED)
# ==========================================

cm = confusion_matrix(y_test, y_pred)

cm_norm = cm.astype("float") / cm.sum(axis=1)[:, None]

plt.figure(figsize=(6,5))

sns.heatmap(
    cm_norm,
    annot=True,
    fmt=".2f",
    cmap="Blues",
    xticklabels=target_encoder.classes_,
    yticklabels=target_encoder.classes_
)

plt.title("Normalized Confusion Matrix")
plt.xlabel("Predicted Race")
plt.ylabel("Actual Race")

plt.tight_layout()

confusion_path = f"{output_folder}\\confusion_matrix.png"
plt.savefig(confusion_path, dpi=300)

plt.show()
plt.close()

print("Confusion matrix saved:", confusion_path)


# ==========================================
# SAVE PREDICTIONS
# ==========================================

results_df = X_test.copy()

results_df["actual_race"] = target_encoder.inverse_transform(y_test)
results_df["predicted_race"] = target_encoder.inverse_transform(y_pred)

prediction_path = f"{output_folder}\\race_predictions.csv"
results_df.to_csv(prediction_path, index=False)

print("Predictions saved:", prediction_path)


# ==========================================
# ACCURACY BY ETHNICITY
# ==========================================

results = results_df.copy()
results["race"] = df.loc[X_test.index, "race"]

ethnicity_accuracy = []

for race in results["race"].unique():

    subset = results[results["race"] == race]

    acc = (subset["actual_race"] == subset["predicted_race"]).mean()

    ethnicity_accuracy.append({
        "race": race,
        "accuracy": acc,
        "count": len(subset)
    })

ethnicity_df = pd.DataFrame(ethnicity_accuracy)

print("\nAccuracy by ethnicity:")
print(ethnicity_df)


# ==========================================
# ETHNICITY ACCURACY CHART
# ==========================================

plt.figure(figsize=(8,5))

sns.barplot(
    data=ethnicity_df,
    x="race",
    y="accuracy",
    hue="count",
    dodge=False
)

plt.title("Prediction Accuracy by Ethnicity")
plt.xlabel("Ethnicity")
plt.ylabel("Accuracy")

plt.xticks(rotation=30)
plt.ylim(0,1)

plt.legend(title="Sample Size")

plt.tight_layout()

ethnicity_path = f"{output_folder}\\ethnicity_accuracy.png"
plt.savefig(ethnicity_path, dpi=300)

plt.show()
plt.close()

print("Ethnicity chart saved:", ethnicity_path)