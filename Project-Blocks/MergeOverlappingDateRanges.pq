let
    Source = (Parameter1 as number) => let
        Source = Sql.Database(#SQL_DATABASE, #SQL_DATABASE", Query=#SQL_CODE),
        #"Run Python script1" = Python.Execute("import pandas as pd#(lf)from datetime import datetime#(lf)#(lf)#(lf)# Wczytaj plik CSV#(lf)df = dataset#(lf)#(lf)# Konwersja kolumn datowych do formatu datetime#(lf)df['Start'] = pd.to_datetime(df['Start'])#(lf)df['End'] = pd.to_datetime(df['End'])#(lf)#(lf)# Sortowanie danych wg ID i daty początkowej#(lf)df = df.sort_values(by=['ID', 'Start'])#(lf)#(lf)# Funkcja do łączenia nakładających się przedziałów#(lf)def merge_intervals(group):#(lf)    merged = []#(lf)    group = group.sort_values(by='Start')#(lf)    #(lf)    current_start = group.iloc[0]['Start']#(lf)    current_end = group.iloc[0]['End']#(lf)    #(lf)#(lf)    for i in range(1, len(group)):#(lf)        row = group.iloc[i]#(lf)        if row['Start'] <= current_end:#(lf)            # Złączenie przedziałów#(lf)            current_end = max(current_end, row['End'])#(lf)            #(lf)        else:#(lf)            # Dodanie zakończonego przedziału#(lf)            merged.append({#(lf)                'ID': group.iloc[0]['ID'],#(lf)                'Start Date': current_start,#(lf)                'End Date': current_end,#(lf)                #(lf)            })#(lf)            # Resetowanie dla nowego przedziału#(lf)            current_start = row['Start']#(lf)            current_end = row['End']#(lf)            #(lf)#(lf)    # Dodanie ostatniego przedziału#(lf)    merged.append({#(lf)        'ID': group.iloc[0]['ID'],#(lf)        'Start Date': current_start,#(lf)        'End Date': current_end,#(lf)        #(lf)    })#(lf)#(lf)    return pd.DataFrame(merged)#(lf)#(lf)# Grupowanie po ID i zastosowanie funkcji merge_intervals#(lf)result = df.groupby('ID').apply(merge_intervals).reset_index(drop=True)#(lf)#(lf)#(lf)# Zapisz wynik do pliku Excel#(lf)result#(lf)",[dataset=Source]),
        result = #"Run Python script1"{[Name="result"]}[Value],
        #"Changed Type" = Table.TransformColumnTypes(result,{{"Start Date", type date}, {"End Date", type date},  {"ID", type text}}),
        #"Trimmed Text" = Table.TransformColumns(#"Changed Type",{{"ID", Text.Trim, type text}}),
        #"Added Index" = Table.AddIndexColumn(#"Trimmed Text", "Index", 0, 1, Int64.Type),
            #"Adjusted End Date" = Table.TransformColumns(#"Added Index", {"End Date", each Date.AddDays(_, -Parameter1), type date}),
        #"Filtered Rows" = Table.SelectRows(#"Adjusted End Date", each [Start Date] <= DateTime.Date(DateTime.LocalNow())),
        #"Filtered Rows1" = Table.SelectRows(#"Filtered Rows", each [End Date] >= DateTime.Date(DateTime.LocalNow())),
        #"Added Custom" = Table.AddColumn(#"Filtered Rows1", "Today", each DateTime.Date(DateTime.LocalNow())),
        #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom",{{"Today", type date}}),
        #"Added Custom1" = Table.AddColumn(#"Changed Type1", "Current days on contracts in row (without a break longer than "& Text.From(Parameter1) &" days)", each Duration.Days([Today] - [Start Date]))
    in
        #"Added Custom1"
in
    Source