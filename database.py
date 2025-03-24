from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use 'mysql+aiomysql://' instead of 'mysql+pymysql://'
DATABASE_URL = "mysql+aiomysql://user:password@127.0.0.1:3307/my_db"

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create an async session factory
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base class for models
Base = declarative_base()

# Dependency to get async DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
