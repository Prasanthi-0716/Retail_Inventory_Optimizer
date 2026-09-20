import pandas as pd
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ==========================================
# 1. Load Processed Dataset
# ==========================================

data = pd.read_csv(
    "data/processed_data.csv",
    low_memory=False
)

print("Dataset loaded successfully.")
print("Original shape:", data.shape)


# ==========================================
# 2. Keep Only Open Stores
# ==========================================

if "Open" in data.columns:
    data = data[data["Open"] == 1].copy()

print("After filtering open stores:", data.shape)


# ==========================================
# 3. Separate Features and Target
# ==========================================

X = data.drop(columns=["Sales"])

y = data["Sales"]


# ==========================================
# 4. Remove Customers
# ==========================================

if "Customers" in X.columns:
    X = X.drop(columns=["Customers"])


# ==========================================
# 5. Identify Categorical Columns
# ==========================================

categorical_columns = X.select_dtypes(
    include=["object"]
).columns.tolist()


for column in categorical_columns:
    X[column] = X[column].astype(str)


# ==========================================
# 6. Identify Numeric Columns
# ==========================================

numeric_columns = X.select_dtypes(
    exclude=["object"]
).columns.tolist()


print("\nCategorical columns:")
print(categorical_columns)

print("\nNumeric columns:")
print(numeric_columns)


# ==========================================
# 7. Create Preprocessor
# ==========================================

preprocessor = ColumnTransformer(

    transformers=[

        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_columns
        ),

        (
            "numeric",
            "passthrough",
            numeric_columns
        )

    ]
)


# ==========================================
# 8. Chronological Train-Test Split
# ==========================================

split_index = int(len(X) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# ==========================================
# 9. Fit Preprocessor
# ==========================================

print("\nFitting preprocessor...")

X_train_processed = preprocessor.fit_transform(
    X_train
)

X_test_processed = preprocessor.transform(
    X_test
)

print("Preprocessing completed.")


# ==========================================
# 10. Random Forest Model
# ==========================================

print("\nCreating Random Forest model...")

model = RandomForestRegressor(

    n_estimators=50,

    random_state=42,

    n_jobs=-1,

    max_depth=20,

    min_samples_leaf=2
)


# ==========================================
# 11. Train Model
# ==========================================

print("Training model...")

model.fit(
    X_train_processed,
    y_train
)

print("Model training completed.")


# ==========================================
# 12. Predictions
# ==========================================

print("\nGenerating predictions...")

y_pred = model.predict(
    X_test_processed
)


# ==========================================
# 13. Evaluation
# ==========================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred
    )
)

r2 = r2_score(
    y_test,
    y_pred
)


# ==========================================
# 14. Display Results
# ==========================================

print("\n==========================================")
print("MODEL EVALUATION RESULTS")
print("==========================================")

print(
    f"MAE  : {mae:.2f}"
)

print(
    f"RMSE : {rmse:.2f}"
)

print(
    f"R2   : {r2:.4f}"
)

print("==========================================")


# ==========================================
# 15. Save Model
# ==========================================

joblib.dump(
    model,
    "models/sales_forecasting_model.joblib"
)

print(
    "\nModel saved:"
)

print(
    "models/sales_forecasting_model.joblib"
)


# ==========================================
# 16. Save Preprocessor
# ==========================================

joblib.dump(
    preprocessor,
    "models/preprocessor.joblib"
)

print(
    "Preprocessor saved:"
)

print(
    "models/preprocessor.joblib"
)


# ==========================================
# 17. Save Evaluation Results
# ==========================================

evaluation_results = {

    "MAE": float(mae),

    "RMSE": float(rmse),

    "R2": float(r2)

}


joblib.dump(
    evaluation_results,
    "models/evaluation_results.joblib"
)

print(
    "Evaluation results saved:"
)

print(
    "models/evaluation_results.joblib"
)


print("\nTraining process completed successfully.")