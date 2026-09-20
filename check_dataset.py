import pandas as pd

# Load datasets
train = pd.read_csv("data/train.csv")
store = pd.read_csv("data/store.csv")

print("========== TRAIN DATA ==========")

print("\nFirst 5 rows:")
print(train.head())

print("\nShape:")
print(train.shape)

print("\nColumns:")
print(train.columns.tolist())

print("\nData Types:")
print(train.dtypes)

print("\nMissing Values:")
print(train.isnull().sum())

print("\nDuplicate Rows:")
print(train.duplicated().sum())


print("\n\n========== STORE DATA ==========")

print("\nFirst 5 rows:")
print(store.head())

print("\nShape:")
print(store.shape)

print("\nColumns:")
print(store.columns.tolist())

print("\nData Types:")
print(store.dtypes)

print("\nMissing Values:")
print(store.isnull().sum())

print("\nDuplicate Rows:")
print(store.duplicated().sum())


print("\n\n========== TARGET INFORMATION ==========")

print("\nSales Statistics:")
print(train["Sales"].describe())

print("\nNumber of Stores:")
print(train["Store"].nunique())

print("\nDate Range:")
print(train["Date"].min(), "to", train["Date"].max())