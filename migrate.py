import sqlite3

# Koneksi ke database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Cek apakah kolom description sudah ada
cursor.execute("PRAGMA table_info(items)")
columns = [column[1] for column in cursor.fetchall()]

# Tambahkan kolom description jika belum ada
if 'description' not in columns:
    cursor.execute('ALTER TABLE items ADD COLUMN description TEXT')
    print("✅ Kolom 'description' berhasil ditambahkan!")

# Tambahkan kolom created_at jika belum ada
if 'created_at' not in columns:
    cursor.execute('ALTER TABLE items ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    print("✅ Kolom 'created_at' berhasil ditambahkan!")

conn.commit()
conn.close()

print("✅ Database berhasil diupdate!")
