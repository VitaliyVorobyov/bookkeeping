import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_table(self):

        create_users = (f"CREATE TABLE IF NOT EXISTS Users ("
                        f"user_id INTEGER PRIMARY KEY,"
                        f"user_name VARCHAR(100) NOT NULL)")

        create_categories = (f"CREATE TABLE IF NOT EXISTS Categories ("
                             f"id SERIAL PRIMARY KEY,"
                             f"category_name VARCHAR(100) NOT NULL UNIQUE)")

        create_sub_categories = (f"CREATE TABLE IF NOT EXISTS SubCategories (id SERIAL PRIMARY KEY,"
                                 f"category_id INTEGER REFERENCES Categories(id),"
                                 f"user_id INTEGER REFERENCES Users(user_id),"
                                 f"sub_category_name VARCHAR(100) NOT NULL)")

        create_entries = (f"CREATE TABLE IF NOT EXISTS Entries ("
                          f"id SERIAL PRIMARY KEY,"
                          f"user_id INTEGER REFERENCES Users(user_id),"
                          f"category_id INTEGER REFERENCES Categories(id),"
                          f"sub_category_id INTEGER REFERENCES SubCategories(id),"
                          f"amount INTEGER NOT NULL,"
                          f"created_at TIMESTAMP DEFAULT NOW())")

        add_categories = (f"INSERT INTO Categories (category_name) VALUES ('Доходы 📈'), ('Расходы 📉') "
                          f"ON CONFLICT DO NOTHING")

        await self.connector.execute(create_users)
        await self.connector.execute(create_categories)
        await self.connector.execute(create_sub_categories)
        await self.connector.execute(create_entries)
        await self.connector.execute(add_categories)

    async def add_user(self, user_id, user_name):
        query = f"INSERT INTO Users (user_id, user_name) VALUES ({user_id}, '{user_name}')"\
                f"ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"
        await self.connector.execute(query)

    async def select_sub_category(self, user_id: int, category: int):
        query = (f"SELECT id, sub_category_name FROM SubCategories "
                 f"WHERE category_id = $1 AND user_id =$2")
        return dict(await self.connector.fetch(query, category, user_id))

    async def add_sub_category(self, user_id: int, category_id: int, sub_category_name: str):
        query = (f"INSERT INTO SubCategories (category_id, user_id, sub_category_name) VALUES "
                 f"($1, $2, $3) ON CONFLICT DO NOTHING")
        await self.connector.execute(query, category_id, user_id, sub_category_name)

    async def add_entry(self, user_id: int, category_id: int, sub_category_id: int, amount: int):
        query = (f"INSERT INTO Entries (user_id, category_id, sub_category_id, amount) VALUES "
                 f"($1, $2, $3, $4)")
        await self.connector.execute(query, user_id, category_id, sub_category_id, amount)

    async def stat(self, user_id: int, category_id: int):
        query = (f"SELECT sub_category_name, SUM(amount) AS amount FROM subcategories INNER JOIN entries "
                 f"ON entries.user_id = subcategories.user_id AND entries.sub_category_id = subcategories.id "
                 f"WHERE entries.user_id = $1 "
                 f"AND entries.category_id = $2 GROUP BY sub_category_name")
        return await self.connector.fetch(query, user_id, category_id)

    async def stat_all(self, user_id: int, category_id: int, list_category: list):
        query = (f"SELECT sub_category_name, amount, DATE(created_at) FROM subcategories INNER JOIN entries "
                 f"ON entries.user_id = subcategories.user_id AND entries.sub_category_id = subcategories.id "
                 f"WHERE entries.user_id = $1 AND subcategories.id = ANY($2::int[]) "
                 f"AND entries.category_id = $3")
        return await self.connector.fetch(query, user_id, list_category, category_id)