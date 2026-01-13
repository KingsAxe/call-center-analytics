# src/database/stochastic_call_simulator.py
import psycopg2
import json
import pandas as pd
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

class StochasticCallCenterSimulator:
    def __init__(self):
        # Business physics parameters
        self.persona_frustration_base = {
            'angry': 0.7,
            'loyal': 0.2,
            'elderly': 0.4,
            'business': 0.5,
            'tech_savvy': 0.3,
            'churn_risk': 0.8
        }
        
        self.issue_resolution_base = {
            'billing': 0.6,
            'internet': 0.5,
            'device': 0.7,
            'cancellation': 0.2,
            'upgrade': 0.9
        }
        
        self.persona_churn_base = {
            'angry': 0.8,
            'loyal': 0.1,
            'elderly': 0.3,
            'business': 0.6,
            'tech_savvy': 0.2,
            'churn_risk': 0.9
        }

    def generate_hidden_state(self):
        """Generate the hidden state first (MANDATORY)"""
        customer_persona = random.choice(['angry', 'loyal', 'elderly', 'business', 'tech_savvy', 'churn_risk'])
        issue_category = random.choice(['billing', 'internet', 'device', 'cancellation', 'upgrade'])
        agent_skill = random.uniform(0.1, 1.0)  # 0.0-1.0 scale
        initial_frustration = random.uniform(0.0, 1.0)
        
        # Calculate resolution probability based on agent skill, issue, and persona
        base_resolution = self.issue_resolution_base[issue_category]
        skill_factor = agent_skill
        persona_factor = 1.0 - (self.persona_frustration_base[customer_persona] * 0.3)
        
        resolution_probability = min(1.0, base_resolution * skill_factor * persona_factor)
        
        # Calculate churn risk
        base_churn = self.persona_churn_base[customer_persona]
        frustration_factor = initial_frustration * 0.4
        churn_risk = min(1.0, base_churn + frustration_factor)
        
        return {
            'customer_persona': customer_persona,
            'issue_category': issue_category,
            'agent_skill': agent_skill,
            'initial_frustration': initial_frustration,
            'resolution_probability': resolution_probability,
            'churn_risk': churn_risk
        }

    def simulate_conversation(self, hidden_state):
        """Simulate emotional state and generate conversation"""
        persona = hidden_state['customer_persona']
        issue = hidden_state['issue_category']
        agent_skill = hidden_state['agent_skill']
        frustration = hidden_state['initial_frustration']
        resolution_prob = hidden_state['resolution_probability']
        
        transcript = []
        resolved = False
        escalated = False
        turns = 0
        max_turns = random.randint(3, 12)
        
        # Initial problem statement
        if issue == 'billing':
            problem = {
                'angry': "My bill is completely wrong and I demand you fix it RIGHT NOW!",
                'loyal': "I noticed some unusual charges on my bill and wanted to check them.",
                'elderly': "I don't understand these charges on my bill, dear.",
                'business': "There are unauthorized charges on my corporate account that need immediate attention.",
                'tech_savvy': "I've identified billing discrepancies that require correction.",
                'churn_risk': "This is exactly why I'm cancelling - your billing is a mess!"
            }[persona]
        elif issue == 'internet':
            problem = {
                'angry': "My internet has been down for HOURS! I pay for reliable service!",
                'loyal': "My connection has been spotty lately. Any idea what's happening?",
                'elderly': "The internet isn't working properly. I can't get my emails.",
                'business': "Internet is down and it's affecting my business operations. Need immediate fix.",
                'tech_savvy': "I'm seeing significant packet loss and high latency. Check your infrastructure.",
                'churn_risk': "This is why I'm leaving - your service is unreliable!"
            }[persona]
        elif issue == 'device':
            problem = {
                'angry': "Your device doesn't work and your instructions are garbage!",
                'loyal': "I'm having trouble setting up my new device. Can you help?",
                'elderly': "I can't figure out how to use this new phone. It's too complicated.",
                'business': "New device isn't working properly. Need it fixed for tomorrow's presentation.",
                'tech_savvy': "I'm experiencing firmware configuration issues.",
                'churn_risk': "Your equipment is junk. This is why I'm switching!"
            }[persona]
        elif issue == 'cancellation':
            problem = {
                'angry': "I'm cancelling IMMEDIATELY! Your service is absolutely terrible!",
                'loyal': "I need to cancel my service. Circumstances have changed.",
                'elderly': "I think I need to cancel some services. I don't use them all.",
                'business': "I'm switching providers. Your service doesn't meet our business needs.",
                'tech_savvy': "I'm cancelling due to consistent service quality issues.",
                'churn_risk': "I'm cancelling. I already found a better provider!"
            }[persona]
        else:  # upgrade
            problem = {
                'angry': "I want to upgrade but your process is so frustrating!",
                'loyal': "I'd like to upgrade my plan. What options do you have?",
                'elderly': "I was told I could upgrade. Can you help me with that?",
                'business': "I need to upgrade for business expansion. What's available?",
                'tech_savvy': "I want to upgrade to the highest speed plan.",
                'churn_risk': "I'll consider upgrading if you can fix these issues."
            }[persona]
        
        transcript.append({"speaker": "Customer", "text": problem})
        
        # Agent greeting
        agent_name = random.choice(['Sarah', 'Mike', 'Jennifer', 'David', 'Alex', 'Taylor'])
        agent_greeting = f"Thank you for calling. This is {agent_name}. How can I assist you today?"
        transcript.append({"speaker": "Agent", "text": agent_greeting})
        
        # Simulate conversation turns
        resolution_achieved = random.random() < resolution_prob
        resolution_progress = 0.0
        
        while turns < max_turns:
            turns += 1
            
            # Update frustration: increases with delay, decreases with reassurance/resolution
            frustration += 0.08  # Delay factor
            
            # Agent response based on skill level
            if agent_skill > 0.7:  # High skill
                if resolution_progress < 0.8 and resolution_achieved:
                    agent_response = self.high_skill_response(issue, agent_skill, resolution_progress)
                    resolution_progress += 0.15
                    frustration -= 0.12  # Reassurance reduces frustration
                else:
                    agent_response = self.high_skill_no_progress_response(issue, agent_skill)
            elif agent_skill > 0.4:  # Medium skill
                if resolution_progress < 0.6 and resolution_achieved and random.random() < 0.7:
                    agent_response = self.medium_skill_response(issue, agent_skill, resolution_progress)
                    resolution_progress += 0.1
                    frustration -= 0.08
                else:
                    agent_response = self.medium_skill_no_progress_response(issue, agent_skill)
                    frustration += 0.05
            else:  # Low skill
                agent_response = self.low_skill_response(issue, agent_skill)
                frustration += 0.15  # Low skill increases frustration
            
            transcript.append({"speaker": "Agent", "text": agent_response})
            
            # Customer response based on frustration and persona
            customer_response = self.customer_response(persona, frustration, issue, resolution_progress, resolution_achieved)
            transcript.append({"speaker": "Customer", "text": customer_response})
            
            # Check for escalation based on frustration and persona
            if frustration > 0.85 and persona in ['angry', 'churn_risk', 'business']:
                if random.random() < 0.4:  # High chance of escalation when very frustrated
                    escalated = True
                    break
            
            # Check for resolution
            if resolution_progress > 0.8 and resolution_achieved:
                resolved = True
                break
            
            # Check for early termination (customer hangs up)
            if frustration > 0.95 and random.random() < 0.3:
                transcript.append({"speaker": "Customer", "text": "I'm done with this. Goodbye."})
                break
        
        return transcript, resolved, escalated, resolution_progress

    def high_skill_response(self, issue, skill, progress):
        responses = {
            'billing': [
                "I can see the issue with your bill. Let me correct those charges immediately.",
                "I've located the error in your billing. I'll process a credit for you now.",
                "I understand your concern. Let me review your account and fix this."
            ],
            'internet': [
                "I can see there's an outage in your area. We expect service to be restored soon.",
                "I'm checking your connection status and seeing some network issues.",
                "I can reset your connection remotely to resolve this issue."
            ],
            'device': [
                "Let me guide you through the proper setup steps for your device.",
                "I see the configuration issue. Let me help you fix it.",
                "I can send a technician if we can't resolve this remotely."
            ],
            'cancellation': [
                "Before you go, let me see what I can do to address your concerns.",
                "I'd like to offer you a special promotion to retain your business.",
                "Let me review your account to see if we can improve your service."
            ],
            'upgrade': [
                "I can process that upgrade for you right away.",
                "I'll move you to our premium plan with enhanced features.",
                "Let me upgrade your service with the latest options."
            ]
        }
        return random.choice(responses[issue])

    def high_skill_no_progress_response(self, issue, skill):
        return random.choice([
            "Let me transfer you to a specialist who can better assist.",
            "I need to escalate this to our technical team for review.",
            "I'm consulting with our experts to find the best solution."
        ])

    def medium_skill_response(self, issue, skill, progress):
        responses = {
            'billing': [
                "I see the issue in your account. Let me look into this for you.",
                "I can help with billing questions. Let me pull up your information.",
                "I need to check your account details to address this."
            ],
            'internet': [
                "Let me check the status in your area regarding service.",
                "I can see your connection history and recent issues.",
                "I'm reviewing your service status to identify the problem."
            ],
            'device': [
                "Let me walk you through some troubleshooting steps.",
                "I can help you with device setup. What model do you have?",
                "Let me check if there are known issues with your device."
            ],
            'cancellation': [
                "I understand you're considering cancellation. Can you tell me more?",
                "I'd like to understand your concerns before you make that decision.",
                "Before you cancel, let me see what options we have."
            ],
            'upgrade': [
                "I can help you upgrade your service. What features are you looking for?",
                "Let me check what upgrade options are available for you.",
                "I can process an upgrade if that's what you're interested in."
            ]
        }
        return random.choice(responses[issue])

    def medium_skill_no_progress_response(self, issue, skill):
        return random.choice([
            "I'm still looking into this for you.",
            "Let me continue checking on this issue.",
            "I need more time to resolve your concern."
        ])

    def low_skill_response(self, issue, skill):
        return random.choice([
            "Let me pull up your account...",
            "I'll need to check on that for you.",
            "Can you repeat your account number?",
            "Let me see what I can find here.",
            "I have to look this up in our system."
        ])

    def customer_response(self, persona, frustration, issue, progress, resolved):
        if frustration > 0.8:
            if persona == 'angry':
                return random.choice([
                    "This is taking forever! Fix it NOW!",
                    "I don't have time for this! Just solve the problem!",
                    "You people are incompetent! This is ridiculous!"
                ])
            elif persona == 'business':
                return random.choice([
                    "I need this resolved immediately. This affects my business.",
                    "This is wasting my time. I have deadlines to meet.",
                    "I expect better service from a professional provider."
                ])
            else:
                return random.choice([
                    "I'm getting frustrated with this process.",
                    "This is taking too long to resolve.",
                    "I'm not happy with how this is progressing."
                ])
        elif frustration > 0.5:
            if persona == 'angry':
                return random.choice([
                    "This is not acceptable!",
                    "Why is this so difficult?",
                    "I'm losing patience here!"
                ])
            else:
                return random.choice([
                    "This is taking longer than expected.",
                    "I hope this gets resolved soon.",
                    "I'm getting concerned about this."
                ])
        else:
            if persona == 'loyal':
                return random.choice([
                    "Thank you for your help. I appreciate it.",
                    "I understand these things happen sometimes.",
                    "I'm glad you're working on this for me."
                ])
            elif persona == 'tech_savvy':
                return random.choice([
                    "Can you provide more technical details about the fix?",
                    "What's the root cause of this issue?",
                    "Will this prevent future occurrences?"
                ])
            else:
                return random.choice([
                    "Okay, thank you for checking on that.",
                    "I appreciate you looking into this.",
                    "That's helpful information, thanks."
                ])

    def calculate_metrics(self, hidden_state, transcript, resolved, escalated, resolution_progress):
        """Calculate duration, CSAT, and churn based on conversation dynamics"""
        persona = hidden_state['customer_persona']
        agent_skill = hidden_state['agent_skill']
        issue = hidden_state['issue_category']
        base_frustration = hidden_state['initial_frustration']
        
        # Duration based on turns and issue complexity
        base_duration = len(transcript) * random.randint(25, 45)
        if issue in ['cancellation', 'billing']:
            base_duration = int(base_duration * 1.3)  # More complex issues take longer
        if agent_skill < 0.5:
            base_duration = int(base_duration * 1.2)  # Low skill agents take longer
        
        duration = max(60, min(1200, base_duration))  # 1-20 minutes
        
        # CSAT calculation
        base_csat = 3.0
        if resolved:
            base_csat += 1.0
        else:
            base_csat -= 1.0
        
        if resolution_progress > 0.5:
            base_csat += 0.5
        if escalated:
            base_csat -= 0.5
        
        # Frustration affects CSAT
        if base_frustration > 0.7:
            base_csat -= 0.5
        if len(transcript) > 8:  # Long calls often indicate frustration
            base_csat -= 0.3
        
        csat = max(1, min(5, round(base_csat)))
        
        # Churn calculation
        base_churn = hidden_state['churn_risk']
        if resolved:
            base_churn *= 0.6  # Resolved issues reduce churn
        if persona == 'loyal':
            base_churn *= 0.3  # Loyal customers rarely churn
        if csat < 3:
            base_churn += 0.2
        if escalated:
            base_churn += 0.15
        
        churned = random.random() < base_churn
        
        return duration, int(csat), bool(churned)

    def generate_call(self):
        """Generate a complete call with all required fields"""
        hidden_state = self.generate_hidden_state()
        transcript, resolved, escalated, _ = self.simulate_conversation(hidden_state)
        duration, csat, churned = self.calculate_metrics(hidden_state, transcript, resolved, escalated, 0)
        
        return {
            "call_id": f"CALL_{uuid.uuid4().hex[:8].upper()}",
            "agent_id": f"AGENT_{random.randint(100, 999)}",
            "customer_persona": hidden_state['customer_persona'],
            "issue_category": hidden_state['issue_category'],
            "transcript": transcript,
            "resolved": resolved,
            "escalated": escalated,
            "duration_sec": duration,
            "csat": csat,
            "churned": churned
        }

    def create_database_and_schema(self):
        """Create PostgreSQL database and schema."""
        conn_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'call_center_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'your_password_here'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        # Connect to default database first to create our target database
        conn = psycopg2.connect(
            host=conn_params['host'],
            database='postgres',
            user=conn_params['user'],
            password=conn_params['password'],
            port=conn_params['port']
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"""
            SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{conn_params['database']}';
        """)
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {conn_params['database']};")
            print(f"Database {conn_params['database']} created successfully!")
        
        cursor.close()
        conn.close()
        
        # Now connect to our specific database and create tables
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Drop table if exists and create new one
        cursor.execute("DROP TABLE IF EXISTS call_logs CASCADE;")
        
        # Create table with all the enhanced fields
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
                turns_count INTEGER,
                resolved BOOLEAN,
                escalated BOOLEAN,
                churned BOOLEAN
            );
        """)
        
        # Create indexes for better query performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_call_logs_timestamp ON call_logs(timestamp);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_call_logs_agent_id ON call_logs(agent_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_call_logs_issue_category ON call_logs(issue_category);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_call_logs_csat_score ON call_logs(csat_score);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transcript_gin ON call_logs USING GIN(transcript_json);")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Stochastic Simulation Engine schema created successfully!")

    def calculate_word_counts_from_transcript(self, transcript):
        """Calculate word counts from transcript."""
        agent_words = sum(len(turn['text'].split()) for turn in transcript if turn['speaker'] == 'Agent')
        customer_words = sum(len(turn['text'].split()) for turn in transcript if turn['speaker'] == 'Customer')
        return agent_words, customer_words

    def calculate_talk_ratio(self, agent_words, customer_words):
        """Calculate talk ratio (agent words / customer words)."""
        if customer_words == 0:
            return float('inf') if agent_words > 0 else 1.0
        return agent_words / customer_words

    def generate_clean_text(self, transcript):
        """Generate clean text from transcript."""
        texts = []
        for turn in transcript:
            if turn.get('speaker') in ['Agent', 'Customer']:
                texts.append(turn.get('text', ''))
        return ' '.join(texts)

    def seed_stochastic_data(self, num_records: int = 1000):
        """Seed the PostgreSQL database with stochastic synthetic data."""
        conn_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'call_center_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'your_password_here'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        print(f"Seeding {num_records} stochastic records into PostgreSQL...")
        
        records = []
        simulator = StochasticCallCenterSimulator()
        
        for i in range(num_records):
            call_data = simulator.generate_call()
            
            # Calculate additional metrics from transcript
            agent_words, customer_words = self.calculate_word_counts_from_transcript(call_data['transcript'])
            talk_ratio = self.calculate_talk_ratio(agent_words, customer_words)
            turns_count = len(call_data['transcript'])
            clean_text = self.generate_clean_text(call_data['transcript'])
            
            # Generate timestamp
            days_back = random.randint(1, 90)
            call_time = datetime.now() - timedelta(days=days_back, 
                                                 hours=random.randint(0, 23),
                                                 minutes=random.randint(0, 59))
            
            record = (
                call_data['call_id'],
                call_data['agent_id'],
                f"CUST_{random.randint(5000, 9999)}",
                call_time,
                call_data['duration_sec'],
                json.dumps(call_data['transcript']),
                call_data['csat'],
                call_data['issue_category'],
                call_data['customer_persona'],
                round(random.uniform(0.6, 1.0), 2),
                clean_text,
                agent_words,
                customer_words,
                round(talk_ratio, 2),
                turns_count,
                call_data['resolved'],
                call_data['escalated'],
                call_data['churned']
            )
            records.append(record)
            
            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{num_records} records...")
        
        # Bulk insert for better performance
        insert_query = """
            INSERT INTO call_logs (call_id, agent_id, customer_id, timestamp, duration_sec, 
                                 transcript_json, csat_score, issue_category, customer_persona, 
                                 data_quality_score, clean_text, agent_word_count, 
                                 customer_word_count, talk_ratio, turns_count, resolved, 
                                 escalated, churned)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (call_id) DO UPDATE SET
                agent_id = EXCLUDED.agent_id,
                customer_id = EXCLUDED.customer_id,
                timestamp = EXCLUDED.timestamp,
                duration_sec = EXCLUDED.duration_sec,
                transcript_json = EXCLUDED.transcript_json,
                csat_score = EXCLUDED.csat_score,
                issue_category = EXCLUDED.issue_category,
                customer_persona = EXCLUDED.customer_persona,
                data_quality_score = EXCLUDED.data_quality_score,
                clean_text = EXCLUDED.clean_text,
                agent_word_count = EXCLUDED.agent_word_count,
                customer_word_count = EXCLUDED.customer_word_count,
                talk_ratio = EXCLUDED.talk_ratio,
                turns_count = EXCLUDED.turns_count,
                resolved = EXCLUDED.resolved,
                escalated = EXCLUDED.escalated,
                churned = EXCLUDED.churned;
        """
        
        cursor.executemany(insert_query, records)
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Successfully seeded {num_records} stochastic records into PostgreSQL!")

def main():
    simulator = StochasticCallCenterSimulator()
    
    # Create database and schema
    simulator.create_database_and_schema()
    
    # Seed data
    simulator.seed_stochastic_data(num_records=1000)

if __name__ == "__main__":
    main()