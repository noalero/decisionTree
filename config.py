import sqlalchemy as sa


database_url = "postgresql://NoaLeron:tsmOn8tln@localhost:5432/DecisionTree"
engine: sa.engine = sa.create_engine(database_url)
training_t_name = "TrainingDataPrimaryTable"
feature_t_name = "FeatureTypeTable"
result_t_name = "ResultTable"

