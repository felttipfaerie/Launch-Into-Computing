import pandas as pd

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

from pathlib import Path

file_path = Path(__file__).parent / "adult.data"

columns = [
    "age","workclass","fnlwgt","education","education_num",
    "marital_status","occupation","relationship","race","sex",
    "capital_gain","capital_loss","hours_per_week","native_country","income"
]

df = pd.read_csv(file_path, names=columns, na_values="?", skipinitialspace=True)

print("Initial shape:", df.shape)
print("\nMissing values:")
print(df.isna().sum())


# --------------------------------------------------
# DEFINE FEATURES
# --------------------------------------------------

target = "education"

X = df.drop(columns=[target])
y = df[target]


# --------------------------------------------------
# PREPROCESSING
# --------------------------------------------------

numerical_cols = X.select_dtypes(include=["int64", "float64"]).columns
categorical_cols = X.select_dtypes(include=["object"]).columns

numerical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numerical_pipeline, numerical_cols),
    ("cat", categorical_pipeline, categorical_cols)
])


# --------------------------------------------------
# TRAIN TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)


# --------------------------------------------------
# MODEL PIPELINE
# --------------------------------------------------

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", DecisionTreeClassifier(max_depth=6, random_state=42))
])

model.fit(X_train, y_train)


# --------------------------------------------------
# OVERALL RESULTS
# --------------------------------------------------

predictions = model.predict(X_test)

print("\nOverall Accuracy:", accuracy_score(y_test, predictions))


# --------------------------------------------------
# CONFUSION MATRICES BY ETHNICITY
# --------------------------------------------------

education_levels = sorted(y.unique())

races = [
    "White",
    "Asian-Pac-Islander",
    "Amer-Indian-Eskimo",
    "Other",
    "Black"
]

for race in races:

    mask = X_test["race"] == race

    X_race = X_test[mask]
    y_race = y_test[mask]

    if len(X_race) == 0:
        continue

    pred_race = model.predict(X_race)

    matrix = confusion_matrix(y_race, pred_race, labels=education_levels)

    matrix_df = pd.DataFrame(
        matrix,
        index=[f"Actual: {e}" for e in education_levels],
        columns=[f"Predicted: {e}" for e in education_levels]
    )

    print("\n==============================")
    print(f"Confusion Matrix for {race}")
    print(f"Samples: {len(X_race)}")
    print("==============================")

    print(matrix_df)