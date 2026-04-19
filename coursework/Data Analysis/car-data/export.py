import pandas as pd

# Store your results
results = {
    "buying": {
        "accuracy": 0.06647398843930635,
        "confusion_matrix": [
            [3, 51, 24, 14],
            [34, 13, 36, 0],
            [43, 34, 0, 0],
            [72, 10, 5, 7]
        ],
        "report": [
            ["0", 0.02, 0.03, 0.02, 92],
            ["1", 0.12, 0.16, 0.14, 83],
            ["2", 0.00, 0.00, 0.00, 77],
            ["3", 0.33, 0.07, 0.12, 94]
        ]
    },

    "maint": {
        "accuracy": 0.07225433526011561,
        "confusion_matrix": [
            [7, 39, 15, 14],
            [55, 6, 35, 2],
            [57, 20, 0, 3],
            [75, 4, 2, 12]
        ],
        "report": [
            ["0", 0.04, 0.09, 0.05, 75],
            ["1", 0.09, 0.06, 0.07, 98],
            ["2", 0.00, 0.00, 0.00, 80],
            ["3", 0.39, 0.13, 0.19, 93]
        ]
    },

    "doors": {
        "accuracy": 0.014450867052023121,
        "confusion_matrix": [
            [4, 64, 11, 4],
            [67, 1, 15, 7],
            [59, 16, 0, 11],
            [66, 15, 6, 0]
        ],
        "report": [
            ["0", 0.02, 0.05, 0.03, 83],
            ["1", 0.01, 0.01, 0.01, 90],
            ["2", 0.00, 0.00, 0.00, 86],
            ["3", 0.00, 0.00, 0.00, 87]
        ]
    },

    "persons": {
        "accuracy": 0.21676300578034682,
        "confusion_matrix": [
            [55, 57, 14],
            [39, 14, 50],
            [50, 61, 6]
        ],
        "report": [
            ["0", 0.38, 0.44, 0.41, 126],
            ["1", 0.11, 0.14, 0.12, 103],
            ["2", 0.09, 0.05, 0.06, 117]
        ]
    },

    "lug_boot": {
        "accuracy": 0.10404624277456648,
        "confusion_matrix": [
            [16, 85, 14],
            [92, 9, 17],
            [75, 27, 11]
        ],
        "report": [
            ["0", 0.09, 0.14, 0.11, 115],
            ["1", 0.07, 0.08, 0.08, 118],
            ["2", 0.26, 0.10, 0.14, 113]
        ]
    },

    "safety": {
        "accuracy": 0.2774566473988439,
        "confusion_matrix": [
            [39, 48, 34],
            [49, 35, 23],
            [76, 20, 22]
        ],
        "report": [
            ["0", 0.24, 0.32, 0.27, 121],
            ["1", 0.34, 0.33, 0.33, 107],
            ["2", 0.28, 0.19, 0.22, 118]
        ]
    },

    "class": {
        "accuracy": 0.9682080924855492,
        "confusion_matrix": [
            [76, 6, 1, 0],
            [1, 10, 0, 0],
            [0, 0, 235, 0],
            [1, 2, 0, 14]
        ],
        "report": [
            ["0", 0.97, 0.92, 0.94, 83],
            ["1", 0.56, 0.91, 0.69, 11],
            ["2", 1.00, 1.00, 1.00, 235],
            ["3", 1.00, 0.82, 0.90, 17]
        ]
    }
}

# Create Excel file
writer = pd.ExcelWriter("car_model_results.xlsx", engine="openpyxl")

for name, data in results.items():

    # Accuracy table
    accuracy_df = pd.DataFrame({"Accuracy": [data["accuracy"]]})

    # Confusion matrix table
    cm_df = pd.DataFrame(data["confusion_matrix"])

    # Classification report table
    report_df = pd.DataFrame(
        data["report"],
        columns=["Class", "Precision", "Recall", "F1-score", "Support"]
    )

    # Write tables to sheet
    accuracy_df.to_excel(writer, sheet_name=name, startrow=0, index=False)
    cm_df.to_excel(writer, sheet_name=name, startrow=3, index=False)
    report_df.to_excel(writer, sheet_name=name, startrow=10, index=False)

writer.close()

print("Spreadsheet saved as car_model_results.xlsx")