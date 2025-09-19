# test_bad.py

def get_db_connection():
    # 🚨 하드코딩된 비밀번호 (보안 규칙 위반)
    password = "123456"
    user = "admin"
    host = "localhost"

    # 여기는 단순 예시니까 실제 DB 연결은 안 함
    return f"mysql://{user}:{password}@{host}/mydb"

if __name__ == "__main__":
    conn = get_db_connection()
    print("DB connection string:", conn)


