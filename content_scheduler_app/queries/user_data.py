import os
import datetime
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not defined!")

engine = create_engine(DATABASE_URL, echo=True)

# The purpose of the Engine is to connect to the database by providing a Connection object.
# When working with the Core directly, the Connection object is how all interaction with
# the database is done. Because the Connection creates an open resource against the database,
# we want to limit our use of this object to a specific context. The best way to do that is with
# a Python context manager, also known as the with statement.

# There are two main methods that can be used to create a connection in the engine.
# (i.) .connect() works as a transaction. The result of the execution is not committed
#       Really, a ROLLBACK is emitted after the execution resulting in not save of the transaction.
#       In order to commit this way, the Connection.commit() method must be called after execution.
# (ii.) .begin() allows for an executed expression to be committed after execution

# with engine.connect() as test:
    # Once the connection is created to the database
    # Executes SQL query to database to insert new resource.
    # test.execute(

        # converts string value to SQL expression value to be executed in database
        # text returns .textClause object as first argument to SQL expression execute method
        # text("INSERT INTO content_scheduler.user VALUES (:id, :username, :password, :email, :created_at, :is_admin)",),

        # The second argument of the .execute() method is the data that will
        # replace the placeholder values in the SQL expression.
        #     [{
        #         "id": 1,
        #         "username": "ethan",
        #         "password": "abcdefgh",
        #         "email": "ethan@gmail.com",
        #         "created_at": datetime.datetime.now(),
        #         "is_admin": True
        #     }]
        # )

    # The values provided have been successfully entered into the database
    # However, after the SQL expression has executed an INSERT, there is no Result object
    # To ensure that the values were successfully entered into the database, a second expression
    # is required. Which is performed directly after, in the same with scope as the first expression

    # result = test.execute(text(
    #     "SELECT * FROM content_scheduler.user"
    # ))

def get_users():
    with engine.begin() as conn:
        query = conn.execute(
            text("SELECT * FROM content_scheduler.user")
            )
        users = [dict(row._mapping) for row in query.fetchall()]
        return users
