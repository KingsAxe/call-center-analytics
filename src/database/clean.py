# clean_and_repopulate.py
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def clean_database():
    """Clean up old data and prepare for new simulation."""
    conn_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'call_center_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'your_password_here'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    # Connect to the database
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    
    print("🔍 Checking current database state...")
    
    # Count existing records
    cursor.execute("SELECT COUNT(*) FROM call_logs;")
    current_count = cursor.fetchone()[0]
    print(f"📊 Current record count: {current_count}")
    
    # Show sample of current data
    cursor.execute("SELECT call_id, agent_word_count, customer_word_count, turns_count FROM call_logs LIMIT 5;")
    print("📋 Sample of current data:")
    for row in cursor.fetchall():
        print(f"   {row}")
    
    # Drop and recreate the table to ensure clean state
    print("🗑️  Dropping existing table...")
    cursor.execute("DROP TABLE IF EXISTS call_logs CASCADE;")
    
    # Recreate table with proper schema
    print("🏗️  Creating new table structure...")
    cursor.execute("""
        CREATE TABLE call_logs (
            call_id VARCHAR(20) PRIMARY KEY,
            agent_id VARCHAR(20),
            customer_id VARCHAR(20),
            timestamp TIMESTAMP WITH TIME ZONE,
            duration_sec INTEGER,
            transcript_json JSONB,
            csat_score INTEGER CHECK (csat_score >= 1 AND csat_score <= 5),
            issue_category VARCHAR(50),
            customer_persona VARCHAR(50),
            data_quality_score DECIMAL(3,2) DEFAULT 1.00,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            clean_text TEXT,
            agent_word_count INTEGER,
            customer_word_count INTEGER,
            talk_ratio DECIMAL(5,2),
            turns_count INTEGER
        );
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_call_logs_timestamp ON call_logs(timestamp);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_call_logs_agent_id ON call_logs(agent_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_call_logs_issue_category ON call_logs(issue_category);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_call_logs_csat_score ON call_logs(csat_score);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transcript_gin ON call_logs USING GIN(transcript_json);")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("✅ Database cleaned and prepared for new data!")

def verify_clean_state():
    """Verify the database is clean."""
    conn_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'call_center_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'your_password_here'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM call_logs;")
    count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    print(f"✅ Verification: Database now has {count} records (should be 0)")
    return count == 0

if __name__ == "__main__":
    print("🔄 Starting database cleanup and repopulation process...")
    
    # Step 1: Clean the database
    clean_database()
    
    # Step 2: Verify clean state
    if verify_clean_state():
        print("✅ Database is clean. Now running high-fidelity simulation...")
        
        # Step 3: Import and run the new simulation engine
        from src.database.novaconnect_simulation_engine import NovaConnectSimulationEngine
        
        engine = NovaConnectSimulationEngine()
        engine.seed_synthetic_data(num_records=1000)
        
        print("🎉 High-fidelity simulation data has been successfully added!")
        
        # Step 4: Verify new data
        conn_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'call_center_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'your_password_here'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        import pandas as pd
        conn = psycopg2.connect(**conn_params)
        
        # Check new data
        query = """
        SELECT 
            call_id,
            issue_category,
            customer_persona,
            agent_word_count,
            customer_word_count,
            talk_ratio,
            turns_count,
            duration_sec,
            csat_score
        FROM call_logs
        LIMIT 10;
        """
        
        df = pd.read_sql_query(query, conn)
        print(f"\n📋 Sample of new high-fidelity data ({len(df)} records shown):")
        print(df)
        
        print(f"\n📈 New data statistics:")
        print(f"   Agent words - Mean: {df['agent_word_count'].mean():.1f}, Std: {df['agent_word_count'].std():.1f}")
        print(f"   Customer words - Mean: {df['customer_word_count'].mean():.1f}, Std: {df['customer_word_count'].std():.1f}")
        print(f"   Turns count - Mean: {df['turns_count'].mean():.1f}, Std: {df['turns_count'].std():.1f}")
        print(f"   Duration - Mean: {df['duration_sec'].mean():.1f} seconds")
        print(f"   CSAT - Mean: {df['csat_score'].mean():.2f}")
        
        conn.close()
        print("\n✅ Database repopulation complete with high-fidelity data!")
    else:
        print("❌ Database cleanup failed. Please check your connection and try again.")