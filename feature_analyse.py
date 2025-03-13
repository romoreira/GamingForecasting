import pandas as pd

# Carregar CSV
df = pd.read_csv("merged_gaming_data.csv")

# Converter "Time" para datetime corretamente
df["Time"] = pd.to_datetime(df["Time"], format="mixed", errors="coerce")

# Verificar se há valores NaT (não convertidos)
print(df["Time"].isna().sum(), "valores não foram convertidos.")

# Remover valores NaT para evitar problemas no agrupamento
df = df.dropna(subset=["Time"])

# Arredondar para segundos
df["Time"] = df["Time"].dt.floor("S")

# Agrupar os dados
df_filtered = df.groupby(["Time", "Country", "Region", "City"]).agg({
    "Length": ["mean", "min", "max", "std"],  
    "RTT": ["mean", "min", "max", "std"],  
    "target": "first"  
}).reset_index()

# Ajustar os nomes das colunas
df_filtered.columns = ['_'.join(col).rstrip('_') for col in df_filtered.columns]

# Garantir que as colunas numéricas não tenham NaN
num_cols = ["Length_mean", "Length_min", "Length_max", "Length_std",
            "RTT_mean", "RTT_min", "RTT_max", "RTT_std"]

df_filtered[num_cols] = df_filtered[num_cols].apply(pd.to_numeric, errors='coerce')
df_filtered.fillna({"Length_std": 0, "RTT_std": 0}, inplace=True)

print(df_filtered.head(50))
df_filtered.to_csv("filtered_gaming_data.csv", index=False)
