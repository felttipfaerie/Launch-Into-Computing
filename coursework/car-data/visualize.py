import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier


# Dataset location
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, "car.data")

df = pd.read_csv(data_path)

columns = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "class"]
df.columns = columns

# Define the correct logical order for ordinal columns
category_orders = {
    "buying": ["low", "med", "high", "vhigh"],
    "maint": ["low", "med", "high", "vhigh"],
    "doors": ["2", "3", "4", "5more"],
    "persons": ["2", "4", "more"],
    "lug_boot": ["small", "med", "big"],
    "safety": ["low", "med", "high"],
    "class": ["unacc", "acc", "good", "vgood"],
}

encoders = {}

for col in df.columns:
    order = category_orders[col]
    mapping = {label: i for i, label in enumerate(order)}
    df[col] = df[col].map(mapping)
    encoders[col] = order


# Folder for matplotlib outputs
output_dir = os.path.join(script_dir, "matplotlib_results")
os.makedirs(output_dir, exist_ok=True)


# Store accuracy results for summary chart
accuracy_results = {}


for target in columns:
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    accuracy_results[target] = accuracy

    # Get labels in the same order as the encoder uses
    labels = encoders[target]
    label_indices = list(range(len(labels)))

    # Confusion matrices with fixed label order
    cm = confusion_matrix(y_test, y_pred, labels=label_indices)
    cm_normalized = confusion_matrix(
        y_test, y_pred, labels=label_indices, normalize="true"
    )

    report = classification_report(y_test, y_pred)

    # Print results in terminal
    print(f"\n===== Target: {target} =====")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(report)
    print("Confusion Matrix (counts):")
    print(cm)
    print("Confusion Matrix (normalized):")
    print(cm_normalized)

    # Plot normalized confusion matrix
    fig, ax = plt.subplots(figsize=(7, 6))
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm_normalized,
        display_labels=labels
    )
    disp.plot(ax=ax, cmap="Blues", values_format=".2f", colorbar=True)

    ax.set_title(f"Normalized Confusion Matrix - {target}")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save and display image
    cm_path = os.path.join(output_dir, f"{target}_normalized_confusion_matrix.png")
    plt.savefig(cm_path)
    plt.show()
    plt.close(fig)


# Create summary bar chart of accuracies
plt.figure(figsize=(10, 6))
plt.bar(accuracy_results.keys(), accuracy_results.values())
plt.title("Model Accuracy by Target Column")
plt.xlabel("Target Column")
plt.ylabel("Accuracy")
plt.xticks(rotation=45)
plt.tight_layout()

summary_path = os.path.join(output_dir, "accuracy_summary.png")
plt.savefig(summary_path)
plt.show()
plt.close()

print("\nMatplotlib output created in:", output_dir)