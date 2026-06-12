from api.database.base import Base
from api.database.session import engine
from api.database.models.conversation import ConversationMessageDB
from api.database.session import get_db


print("Tables before:")
print(Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)

with engine.connect() as conn:
    result = conn.exec_driver_sql(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        """
    )

    print("\nTables in DB:")
    for row in result:
        print(row[0])

from api.core.config import settings
print(settings.database_url)



from sqlalchemy import text

db = next(get_db())

result = db.execute(
    text("SELECT current_database();")
)

print(result.scalar())