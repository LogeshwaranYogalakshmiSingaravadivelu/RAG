def initialize_database(db_connection):
    cursor = db_connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            document_name VARCHAR(255) NOT NULL,
            document_type VARCHAR(50) NOT NULL,
            full_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_info (
            id SERIAL PRIMARY KEY,
            document_id INTEGER REFERENCES documents(id),
            course_name VARCHAR(255),
            course_number VARCHAR(50),
            section VARCHAR(10),
            semester VARCHAR(50),
            year INTEGER,
            instructor_name VARCHAR(100),
            enrollment_count INTEGER,
            response_count INTEGER,
            declines_count INTEGER
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_ratings (
            id SERIAL PRIMARY KEY,
            document_id INTEGER REFERENCES documents(id),
            category VARCHAR(100),
            question TEXT,
            response_count INTEGER,
            course_mean DECIMAL(3,1)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_comments (
            id SERIAL PRIMARY KEY,
            document_id INTEGER REFERENCES documents(id),
            question_category VARCHAR(100),
            question TEXT,
            comment_number INTEGER,
            comment_text TEXT
        )""")

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_documents_name ON documents(document_name);
        CREATE INDEX IF NOT EXISTS idx_course_info_instructor ON course_info(instructor_name);
        """)

        db_connection.commit()
        print("Database schema initialized successfully")
    except Exception as e:
        db_connection.rollback()
        print(f"Error initializing database: {e}")
