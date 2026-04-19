import pandas as pd
from sklearn.utils import resample
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

# column names for the dataset
columns = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "class"]

# load dataset
df = pd.read_csv("coursework/car-data/car.data", names=columns)

print("Dataset info:")
print(df.info())

print("\nFirst 5 rows:")
print(df.head())

# --------------------------------------------------
# ENCODE CATEGORICAL COLUMNS
# --------------------------------------------------

# use a separate encoder for each column
encoders = {}

for col in df.columns:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])
    encoders[col] = encoder

print("\nEncoded class counts:")
print(df["class"].value_counts().sort_index())

# --------------------------------------------------
# CREATE FEATURES AND TARGET
# --------------------------------------------------

X = df.drop("class", axis=1)
y = df["class"]

# --------------------------------------------------
# SPLIT BEFORE BALANCING
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# combine training features and target for resampling
train_df = pd.concat([X_train, y_train], axis=1)

print("\nTraining class counts before balancing:")
print(train_df["class"].value_counts().sort_index())

print("\nTest class counts (untouched):")
print(y_test.value_counts().sort_index())

# --------------------------------------------------
# BALANCE TRAINING DATA ONLY
# --------------------------------------------------

max_size = train_df["class"].value_counts().max()
balanced_groups = []

for class_value in sorted(train_df["class"].unique()):
    group = train_df[train_df["class"] == class_value]

    upscaled_group = resample(
        group,
        replace=True,
        n_samples=max_size,
        random_state=42
    )

    balanced_groups.append(upscaled_group)

balanced_train_df = (
    pd.concat(balanced_groups)
    .sample(frac=1, random_state=42)
    .reset_index(drop=True)
)

print("\nTraining class counts after balancing:")
print(balanced_train_df["class"].value_counts().sort_index())

# split balanced training data back into X and y
X_train_balanced = balanced_train_df.drop("class", axis=1)
y_train_balanced = balanced_train_df["class"]

# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train_balanced, y_train_balanced)

# --------------------------------------------------
# TEST MODEL
# --------------------------------------------------

y_pred = model.predict(X_test)

# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("\nTarget: class")

accuracy = accuracy_score(y_test, y_pred)
print("\nAccuracy:", accuracy)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))