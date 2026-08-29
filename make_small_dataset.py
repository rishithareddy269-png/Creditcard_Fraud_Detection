import pandas as pd

df = pd.read_csv("creditcard.csv")

fraud = df[df["Class"] == 1]
normal = df[df["Class"] == 0]

normal_sample = normal.sample(
    n=min(10000, len(normal)),
    random_state=42
)

small_df = pd.concat([normal_sample, fraud])

small_df = small_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

small_df.to_csv("creditcard_small.csv", index=False)

print("Small dataset created successfully!")
print("Rows:", len(small_df))
print("Columns:", len(small_df.columns))
print("Fraud transactions:", (small_df["Class"] == 1).sum())