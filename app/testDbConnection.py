from sqlalchemy import create_engine, text
import time

SUPABASE_PASSWORD = "cerveceroyosoyymividasevaacabando"
SUPABASE_URL = f"postgresql://postgres:{SUPABASE_PASSWORD}@db.wshqdpedakskoyqvtwqw.supabase.co:5432/postgres"

def test_connection():
    print("Probando conexión a Supabase...")
    
    try:
        engine = create_engine(SUPABASE_URL, echo=True)
        with engine.connect() as conn:
            # Usar text() para crear una consulta ejecutable
            result = conn.execute(text("SELECT 1"))
            first_result = result.scalar()
            print(f"¡Conexión exitosa! Resultado: {first_result}")
            
            # Probar que podemos ver las tablas
            print("\nListando tablas existentes:")
            tables = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            
            for table in tables:
                print(f"- {table[0]}")
            
            return True
            
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False

if __name__ == "__main__":
    test_connection()