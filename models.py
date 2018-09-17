from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship

from settings import Base, ENGINE


'''Qoo10中間テーブル'''
category_qoo10 = Table('category_qoo10', Base.metadata,
    Column('category_id', Integer, ForeignKey('categories.id')),
    Column('qoo10_category_id', Integer, ForeignKey('qoo10_categories.id'))
)


class Category(Base):
    '''Baseカテゴリーモデル'''

    __tablename__ = 'categories'
    __table_args__ = (UniqueConstraint('name', 'parent_id', name="unique_idx_name_parent"),)

    id = Column(Integer, primary_key=True)
    category_id = Column(String(100), index=True, unique=True)
    name = Column(String(300))
    parent_id = Column(Integer, ForeignKey('categories.id'), index=True, nullable=True, default=None)
    source_url = Column(String(1024))

    parent = relationship(lambda: Category, remote_side=id, backref='sub_categories')
    qoo10_categories = relationship('Qoo10Category', secondary=category_qoo10, back_populates='base_categories')


class Qoo10Category(Base):
    '''Qoo10の標準カテゴリー'''
    __tablename__ = 'qoo10_categories'

    id = Column(Integer, primary_key=True)
    l_category_id = Column(String(20))
    l_category_name = Column(String(100))
    m_category_id = Column(String(20))
    m_category_name = Column(String(100))
    s_category_id = Column(String(20))
    s_category_name = Column(String(100))

    base_categories = relationship('Category', secondary=category_qoo10, back_populates='qoo10_categories')

class Product(Base):
    '''Base商品モデル'''

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_id = Column(String(100), index=True)
    name = Column(String(1024), unique=True)
    description = Column(Text)
    images = Column(String(2024))
    proper_price = Column(Integer)
    sales_price = Column(Integer)
    source_url = Column(String(1024))
    source = Column(String(100), index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), index=True)
    category = relationship('Category', backref='products')

if __name__ == '__main__':
    Base.metadata.create_all(bind=ENGINE)
