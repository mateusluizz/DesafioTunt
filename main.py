import pandas as pd
import numpy as np
from constants import GOOGLE_SHEET_KEY, SOFTWARE_ENGENIERING_PATH, FINAL_RESULTS_PATH
from gspread.exceptions import APIError
from utils import get_sheet_data

try:
    df_data = get_sheet_data(GOOGLE_SHEET_KEY, 'engenharia_de_software')

    # Save the data in csv
    df_data_csv = (
        pd.DataFrame(df_data)
        .to_csv(
            SOFTWARE_ENGENIERING_PATH,
            index=False,
            header=False
        )
    )

    total_semester_classes = (
        pd.DataFrame(df_data[1], columns=['Total'])
        .loc[0, 'Total']
        .split(':')[1].strip()
    )

    # Dataframe with data
    df_data = pd.DataFrame(df_data[3:], columns=df_data[2])

    # Convert the columns with numeric data
    numeric_columns = ['Faltas', 'P1', 'P2', 'P3']
    df_data[numeric_columns] = df_data[numeric_columns].apply(pd.to_numeric)

    print("Incoming data")
    print(df_data)

except (FileNotFoundError, APIError):
    # Read the files locally
    df_data = pd.read_csv(SOFTWARE_ENGENIERING_PATH, skiprows=2)

    total_semester_classes = (
        pd.read_csv(SOFTWARE_ENGENIERING_PATH)
        .iloc[0, 0]
        .split(':')[1].strip()
    )

    numeric_columns = ['Faltas', 'P1', 'P2', 'P3']
    df_data[numeric_columns] = df_data[numeric_columns].apply(pd.to_numeric)

    print("Local data")
    print(df_data)

except Exception as error:
    raise Exception(f'Error: {error}')

df_data['Mean'] = ((df_data['P1'] + df_data['P2'] + df_data['P3']) / 30).round(2)

print('Dataframe with the "Mean" column')
print(df_data)

df_data['Situação'] = (
    np.where(
        df_data['Faltas'] < int(total_semester_classes) * 25 / 100,
        'Reprovado por Falta',
        np.where(
            (df_data['Mean'] >= 7),
            "Aprovado",
            np.where(
                (df_data['Mean'] >= 5) & (df_data['Mean'] < 7),
                "Exame Final",
                "Reprovado por Nota"
            )
        )
    )
)

print('Dataframe with the "Situação" column filled')
print(df_data)

df_data['Nota para Aprovação Final'] = (
    np.where(
        df_data['Situação'] != 'Exame Final',
        0,
        (10 - df_data['Mean']).round(2),
    )
)

print('Dataframe with the "Nota para Aprovação Final" column filled')
print(df_data)

df_data = df_data[['Matricula', 'Aluno', 'Faltas', 'P1', 'P2', 'P3', 'Mean', 'Situação', 'Nota para Aprovação Final']]
df_data.to_csv(FINAL_RESULTS_PATH, index=False)

print('Final results')
print(df_data[['Aluno', 'Faltas', 'Mean', 'Situação', 'Nota para Aprovação Final']])
