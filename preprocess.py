import pandas as pd


# =========================================================
# FILE PATHS
# =========================================================

TRAIN_FILE = "data/train.csv"
STORE_FILE = "data/store.csv"
OUTPUT_FILE = "data/processed_data.csv"


# =========================================================
# LOAD DATA
# =========================================================

print("Loading train.csv...")

train_df = pd.read_csv(
    TRAIN_FILE,
    low_memory=False
)

print("Loading store.csv...")

store_df = pd.read_csv(
    STORE_FILE,
    low_memory=False
)


print("\nTrain shape:", train_df.shape)
print("Store shape:", store_df.shape)


# =========================================================
# MERGE DATASETS
# =========================================================

print("\nMerging datasets...")

df = train_df.merge(
    store_df,
    on="Store",
    how="left"
)


print("Merged shape:", df.shape)


# =========================================================
# DATE PROCESSING
# =========================================================

print("\nProcessing Date column...")

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)


# Remove rows where date is invalid

df = df.dropna(
    subset=["Date"]
)


# =========================================================
# CREATE DATE FEATURES
# =========================================================

df["Year"] = df["Date"].dt.year

df["Month"] = df["Date"].dt.month

df["Day"] = df["Date"].dt.day

df["WeekOfYear"] = (
    df["Date"].dt.isocalendar().week
    .astype(int)
)


# =========================================================
# REMOVE ORIGINAL DATE
# =========================================================

df = df.drop(
    columns=["Date"]
)


# =========================================================
# HANDLE MISSING VALUES
# =========================================================

numeric_columns = df.select_dtypes(
    include=["number"]
).columns


categorical_columns = df.select_dtypes(
    exclude=["number"]
).columns


for column in numeric_columns:

    df[column] = df[column].fillna(
        df[column].median()
    )


for column in categorical_columns:

    df[column] = df[column].fillna(
        "Unknown"
    )


# =========================================================
# SAVE PROCESSED DATA
# =========================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nPreprocessing completed.")

print(
    "Processed file saved to:",
    OUTPUT_FILE
)

print(
    "Final dataset shape:",
    df.shape
)

print(
    "\nColumns:"
)

for column in df.columns:
    print("-", column)