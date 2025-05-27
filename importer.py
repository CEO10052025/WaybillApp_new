import pandas as pd
import sqlite3

def import_excel(file_path: str, table: str, db_file: str = "data/waybills.db"):
    df = pd.read_excel(file_path)
    conn = sqlite3.connect(db_file)
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    df.to_sql(table, conn, if_exists='append', index=False)
    conn.close()
    return df
