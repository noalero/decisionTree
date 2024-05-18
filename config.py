import sqlalchemy as sa


database_url = "postgresql://NoaLeron:tsmOn8tln@localhost:5432/DecisionTree"
engine: sa.engine = sa.create_engine(database_url)
