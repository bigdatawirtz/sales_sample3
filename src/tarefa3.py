"""Tarefa 3: importe total e número de vendas de 2025 a partir de tres ficheiros cuadrimestrais"""
from pathlib import Path
import pandas as pd

carpeta = Path("datos/raw")
ficheiros = sorted(carpeta.glob("vendas_2025_cuadrimestre*.csv"))
assert len(ficheiros) == 3, f"Esperábanse 3 ficheiros e atopáronse {len(ficheiros)}"

def eur(x):
    return f"{x:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

def num(x):
    return f"{x:,}".replace(",", ".")

# 1. Ler os tres ficheiros, indicando de cal vén cada fila
partes = []
for f in ficheiros:
    df = pd.read_csv(f, sep=";", decimal=",", encoding="utf-8")
    assert pd.api.types.is_numeric_dtype(df["importe"]), f"importe non numérico en {f.name}"
    df["orixe"] = f.name
    print(f"{f.name}: {num(len(df))} filas, {df['data'].min()} a {df['data'].max()}, {eur(df['importe'].sum())}")
    partes.append(df)

vendas = pd.concat(partes, ignore_index=True)
print(f"\nSuma directa dos tres ficheiros: {num(len(vendas))} vendas, {eur(vendas['importe'].sum())}")

# 2. Comprobar se hai identificadores repetidos
repetidos = vendas[vendas.duplicated("id_venda", keep=False)]
if repetidos.empty:
    print("Non hai id_venda repetidos.")
else:
    print(f"\nAtención: {num(repetidos['id_venda'].nunique())} id_venda aparecen máis dunha vez")
    print(repetidos.groupby("orixe")["data"].agg(["count", "min", "max"]))

    # Son copias exactas da mesma venda ou vendas distintas co mesmo id?
    columnas = [c for c in vendas.columns if c != "orixe"]
    distintas = repetidos.drop_duplicates(subset=columnas)["id_venda"].duplicated().sum()
    print(f"id repetidos con datos diferentes: {distintas}")
    assert distintas == 0, "Hai id repetidos con datos distintos: revisar á man"

# 3. Eliminar duplicados (quedamos coa primeira aparición de cada id_venda)
unicas = vendas.drop_duplicates("id_venda", keep="first")

print(f"\nNúmero de vendas: {num(len(unicas))}")
print(f"Importe total:    {eur(unicas['importe'].sum())}")
print(f"(Eliminadas {num(len(vendas) - len(unicas))} filas duplicadas, "
      f"{eur(vendas['importe'].sum() - unicas['importe'].sum())})")
