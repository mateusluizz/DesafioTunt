from pathlib import Path
import os

PATH_COMMON = Path(__file__).resolve().parent

CREDENTIALS = Path(__file__).resolve().parent / 'resources/credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(CREDENTIALS)

GOOGLE_SHEET_KEY = '1gE6vC3y6b0ZnTWEBOYcze_xfR12UsxmXK_0rlTNdicw'

SOFTWARE_ENGENIERING_PATH = f'{PATH_COMMON}/output/software_engineering.csv'
FINAL_RESULTS_PATH = f'{PATH_COMMON}/output/final_results.csv'
