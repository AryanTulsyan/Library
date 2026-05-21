import psycopg2

# We are using the exact string you provided
dsn = "postgres://neondb_owner:npg_bmY4hc5BpWGR@ep-sparkling-dawn-ap0phkrd.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require"

try:
    conn = psycopg2.connect(dsn)
    print("🚀 SUCCESS: Successfully connected to Neon PostgreSQL!")
    conn.close()
except Exception as e:
    print(f"❌ CONNECTION FAILED:\n{e}")