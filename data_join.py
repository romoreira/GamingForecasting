import os
import pandas as pd

# Diretório base onde os CSVs estão armazenados
base_dir = "GAViST5G/GAViST5G/Global/Online Gaming"


# Lista para armazenar os DataFrames carregados
dataframes = []

# Percorrer todas as pastas (LOL, TFT, VAL)
for game in os.listdir(base_dir):
    game_path = os.path.join(base_dir, game)
    
    # Garantir que seja um diretório antes de processar
    if os.path.isdir(game_path):
        # Percorrer todos os arquivos CSV dentro da pasta do jogo
        for file in os.listdir(game_path):
            if file.endswith(".csv"):
                file_path = os.path.join(game_path, file)
                
                # Carregar CSV
                df = pd.read_csv(file_path)
                
                # Adicionar coluna 'target' com o nome do jogo
                df["target"] = game
                
                # Adicionar ao conjunto de DataFrames
                dataframes.append(df)

# Concatenar todos os DataFrames em um único
merged_df = pd.concat(dataframes, ignore_index=True)

# Remover duplicatas baseadas em colunas como (Source, Destination, Protocol, Time)
merged_df = merged_df.drop_duplicates(subset=["Source", "Destination", "Protocol", "Time"])

# Salvar dataset consolidado
merged_df.to_csv("merged_gaming_data.csv", index=False)

print("Dataset consolidado salvo como 'merged_gaming_data.csv'.")
