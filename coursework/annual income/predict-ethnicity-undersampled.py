import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

file_path = Path(__file__).parent / "adult.data"

columns = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"
]

df = pd.read_csv(
    file_path,
    names=columns,
    na_values="?",
    skipinitialspace=True
)

print("Initial shape:", df.shape)
print("\nMissing values:")
print(df.isna().sum())


# --------------------------------------------------
# VISUALIZATIONS - ORIGINAL DATA
# --------------------------------------------------

output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)

# 1. Distribution of occupation (Original Data)
occupation_counts = df["occupation"].fillna("Missing").value_counts().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
occupation_counts.plot(kind="bar")
plt.title("Distribution of Occupation (Original Data)")
plt.xlabel("Occupation")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(output_dir / "distribution_of_occupation_original_data.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()

# 2. Distribution of race (Original Data)
race_counts = df["race"].fillna("Missing").value_counts().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
race_counts.plot(kind="bar")
plt.title("Distribution of Race (Original Data)")
plt.xlabel("Race")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(output_dir / "distribution_of_race_original_data.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()


# --------------------------------------------------
# DEFINE FEATURES
# --------------------------------------------------

target = "race"

X = df.drop(columns=[target])
y = df[target]

print("\nFeatures preview:")
print(X.head())

print("\nTarget preview:")
print(y.head())


# --------------------------------------------------
# PREPROCESSING
# --------------------------------------------------

categorical_features = X.select_dtypes(include=["object"]).columns.tolist()
numeric_features = X.select_dtypes(exclude=["object"]).columns.tolist()

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)


# --------------------------------------------------
# TRAIN / TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# MODEL
# --------------------------------------------------

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", DecisionTreeClassifier(random_state=42, max_depth=10))
])

model.fit(X_train, y_train)
y_pred = model.predict(X_test)


# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

labels = sorted(y.unique())
cm = confusion_matrix(y_test, y_pred, labels=labels)


# --------------------------------------------------
# VISUALIZATION - CONFUSION MATRIX
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 8))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot(ax=ax, xticks_rotation=45, colorbar=False)
ax.set_title("Race Prediction (Original Data)")
fig.tight_layout()
fig.savefig(output_dir / "confusion_matrix.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close(fig)


# --------------------------------------------------
# VISUALIZATION - OVERALL PREDICTIONS BAR CHART
# --------------------------------------------------

pred_counts = pd.Series(y_pred).value_counts().reindex(labels, fill_value=0)

plt.figure(figsize=(10, 6))
pred_counts.plot(kind="bar")
plt.title("Bar Chart of Overall Predictions (Original Data)")
plt.xlabel("Predicted Race")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(output_dir / "bar_chart_of_overall_predictions.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()


# --------------------------------------------------
# OPTIONAL: NORMALIZED PREDICTION BAR CHART
# --------------------------------------------------

pred_percent = pred_counts / pred_counts.sum()

plt.figure(figsize=(10, 6))
pred_percent.plot(kind="bar")
plt.title("Normalized Bar Chart of Overall Predictions (Original Data)")
plt.xlabel("Predicted Race")
plt.ylabel("Proportion")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(output_dir / "normalized_bar_chart_of_overall_predictions.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()