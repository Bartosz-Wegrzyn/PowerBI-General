import pandas as pd
from datetime import datetime


# Wczytaj plik CSV
df = dataset

# Konwersja kolumn datowych do formatu datetime
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])

# Sortowanie danych wg ID i daty początkowej
df = df.sort_values(by=['ID', 'Start'])

# Funkcja do łączenia nakładających się przedziałów
def merge_intervals(group):
    merged = []
    group = group.sort_values(by='Start')
    
    current_start = group.iloc[0]['Start']
    current_end = group.iloc[0]['End']
    assignment_count = int(group.iloc[0]['A'])

    for i in range(1, len(group)):
        row = group.iloc[i]
        if row['Start'] <= current_end:
            # Złączenie przedziałów
            current_end = max(current_end, row['End'])
            assignment_count += int(row['A'])
        else:
            # Dodanie zakończonego przedziału
            merged.append({
                'ID': group.iloc[0]['ID'],
                'Start Date': current_start,
                'End Date': current_end,
                'No. of As': assignment_count
            })
            # Resetowanie dla nowego przedziału
            current_start = row['Start']
            current_end = row['End']
            assignment_count = int(row['A'])

    # Dodanie ostatniego przedziału
    merged.append({
        'ID': group.iloc[0]['ID'],
        'Start Date': current_start,
        'End Date': current_end,
        'No. of As': assignment_count
    })

    return pd.DataFrame(merged)

# Grupowanie po ID i zastosowanie funkcji merge_intervals
result = df.groupby('ID').apply(merge_intervals).reset_index(drop=True)

# Podziel kolumnę ID na dwie kolumny Consultant i Client
# Użyj expand=True i ustal domyślną wartość dla Client, gdy ID nie zawiera ":"
split_ids = result['ID'].str.split(':', n=1, expand=True)
split_ids.columns = ['Consultant', 'Client']
result = pd.concat([result, split_ids], axis=1)

# Usuń starą kolumnę ID, jeśli nie jest już potrzebna
result = result.drop(columns=['ID'])

# Zapisz wynik do pliku Excel
result
