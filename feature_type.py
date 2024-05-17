import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = sa.orm.declarative_base()


class FeatureTypeObject(Base):
    __tablename__ = 'FeatureTypeTable'
    rule_id = sa.Column('rule_id', sa.Integer, primary_key=True, autoincrement=True, unique=True)
    feature_type = sa.Column('feature_type', sa.ARRAY(sa.Integer), nullable=False)
    feature_type_value = sa.Column('feature_type_value', sa.ARRAY(sa.Integer), nullable=False)
    __table_args__ = (sa.UniqueConstraint('feature_type', 'feature_type_value', name='uix_feature_type_value'),)
    # [feature_type]: array of integers (indexes in primary table)
    # [feature_type_value]: array of integers (indexes in feature breeds) correlated with [feature_type]
    # [rule_id]: unique id, represent a specific [feature_type_value] of a specific [feature_type]
