from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

SECRET_KEY = "fd2305070b0ecf45c5f4cf83c3302a6a408df2bdcbbabbe0b60ab8c9b0de2c39"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 356

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)