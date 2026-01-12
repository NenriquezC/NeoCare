import psycopg2

# Conectar a PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="neocare",
    user="postgres",
    password="Limon1307"
)

cursor = conn.cursor()

try:
    # Leer el script SQL
    with open('add_timestamps_to_labels_subtasks.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Ejecutar
    cursor.execute(sql)
    conn.commit()
    
    print("✅ Columnas created_at y updated_at agregadas correctamente")
    print("   - labels.created_at")
    print("   - subtasks.created_at")
    print("   - subtasks.updated_at")
    
except Exception as e:
    conn.rollback()
    print(f"❌ Error: {e}")
finally:
    cursor.close()
    conn.close()
