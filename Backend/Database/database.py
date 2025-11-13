from sqlmodel import SQLModel, create_engine

# Define the database URL for the SQLite database
DATABASE_URL = "sqlite:///./tempcastml.db"

# Create a new database engine
# The `echo=False` argument prevents the engine from logging all SQL statements
engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    """
    This function creates the database and all tables defined in the SQLModel metadata.
    """
    SQLModel.metadata.create_all(engine)
