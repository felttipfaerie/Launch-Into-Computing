import pandas as pd

# column names for the dataset
columns = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "class"]

# load dataset
df = pd.read_csv("coursework/data/car+evaluation/car.data", names=columns)

""""The dataset contains the following columns:
# show first rows
print(df.head())
"""

from sklearn.preprocessing import LabelEncoder

""""
# check for missing values
print(df.isnull().sum())
"""

# encode categorical columns
encoder = LabelEncoder()

for col in df.columns:
    df[col] = encoder.fit_transform(df[col])

# predict the following value:
X = df.drop("class", axis=1)
y = df["class"]

""""
print("\nPreprocessed data:")
print(df.head())

print("\nFeatures:")
print(X.head())

print("\nTarget:")
print(y.head())
"""

from sklearn.model_selection import train_test_split

# split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

from sklearn.tree import DecisionTreeClassifier

# create the model
model = DecisionTreeClassifier()

# train the model
model.fit(X_train, y_train)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# make predictions
y_pred = model.predict(X_test)

# class
print("class")

# accuracy score
accuracy = accuracy_score(y_test, y_pred)
print("\nAccuracy:", accuracy)

# confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))