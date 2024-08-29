from passlib.context import CryptContext

# Initialize the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_hashed_password(plain_password: str) -> str:
    """Generate a hashed password using bcrypt."""
    return pwd_context.hash(plain_password)

print(generate_hashed_password("password"))