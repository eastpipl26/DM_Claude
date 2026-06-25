import sqlite3

conn = sqlite3.connect("C:/Users/eastp/voicebox/data/voicebox.db")
cur = conn.cursor()

tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("tables:", [t[0] for t in tables])

for table in [t[0] for t in tables]:
    count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"\n=== {table} ({count} rows) ===")
    rows = cur.execute(f"SELECT * FROM {table} LIMIT 5").fetchall()
    cols = [d[0] for d in cur.description]
    print("cols:", cols)
    for row in rows:
        print(dict(zip(cols, row)))

conn.close()
