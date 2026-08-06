# Scenario 5: Variable 'temp' already renamed to 'userCache'

def load_users_from_db():
    return ["alice", "bob", "charlie"]

def initialize_cache():
    userCache = load_users_from_db()  # previously named 'temp'
    print("Users loaded into cache:", userCache)

initialize_cache()
