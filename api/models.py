from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import json
import redis
import re

"""
# SQLAlchemy setup
Base = declarative_base()
# Replace 'username', 'password', 'host', and 'database' with your MySQL connection details
connection_string = 'mysql+pymysql://username:password@host/database'
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
session = Session()
"""

class Models(object):

    def __init__(self, model):
        self.redis_cache = redis.Redis(host='localhost', port=6379, db=0)
        self.model = model
        self.model_prefix = self.model.__name__
        print("prefix", self.model_prefix)
        
        # SQLAlchemy setup
        self.Base = declarative_base()
        # Replace 'username', 'password', 'host', and 'database' with your MySQL connection details
        connection_string = 'mysql+pymysql://root:root@localhost:3306/shipping'
        self.engine = create_engine(connection_string)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.db_model = self.generate_db_model_class()

    def get(self, key):
        pkey = self.model_prefix + "_" + str(key)
        data =  self.redis_cache.get(pkey)
        if data:
            return self.model.parse_raw(data)
        
        data = self.db_get(key)
        if data:
            self.redis_cache.set(pkey, json.dumps(data))

        try:
            return self.model.parse_raw(json.dumps(data))
        except:
            return None

    def set(self, key, value):
        pkey = self.model_prefix + "_" + str(key)
        if self.db_set(value):
            return self.redis_cache.set(pkey, value)
        else:
            return None

    def update(self, key, value):
        pkey = self.model_prefix + "_" + str(key)
        if self.db_update(value):
            return self.redis_cache.set(pkey, value)
        else:
            return None

    def delete(self, key):
        pkey = self.model_prefix + "_" + str(key)
        if self.db_delete(key):
            return self.redis_cache.delete(pkey)
        else:
            return None

    def db_get(self, key):
        query = self.session.query(self.db_model).get(key)
        if not query:
            return query
        query_dict = query.__dict__
        query_dict = { key:value for key,value in query_dict.items() if key[0] != "_" }
        #query_dict = json.dumps(query_dict)
        return query_dict

    def db_set(self, value):
        try:
            value_dict = json.loads(value)
            table_set = self.db_model(**value_dict)
            self.session.add(table_set)
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def db_update(self, value):
        try:
            value_dict = json.loads(value)
            table_set = self.db_model(**value_dict)
            updated_record = self.session.merge(table_set)
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True


    def db_delete(self, key):
        try:
            query = self.session.query(self.db_model).get(key)
            self.session.delete(query)
            self.session.commit()
        except Exception:
            return False
        return True

    def generate_db_model_class(self):
        class_name = self.model_prefix
        base_classes = (self.Base,) 

        class_attributes = dict()
        fields = self.model.model_fields

        for field  in fields:
            print(field, type(fields[field]))
            value = fields[field]
            print(dir(value))
            vtype = value.annotation
            vreq = True if not value.is_required else False
            if vtype == int:
                if "id" in field:
                    class_attributes[field] = Column(Integer, primary_key=True, index=True)
                else:
                    class_attributes[field] = Column(Integer, nullable=vreq)
            elif vtype == str:
                if "id" in field:
                    class_attributes[field] = Column(String(length=50), primary_key=True, index=True)
                else:
                    class_attributes[field] = Column(String(length=50), nullable=vreq)
        table_name = re.sub(r'(?<!^)(?=[A-Z])', '_', self.model_prefix).lower()
        class_attributes["__tablename__"] = table_name

        db_model = self.create_dynamic_class(class_name, base_classes, class_attributes)
       
        #existing_tables = self.engine.table_names()
        inspector = inspect(self.engine)
        existing_tables = inspector.get_table_names()
        if table_name not in existing_tables:
            self.Base.metadata.create_all(bind=self.engine)

        return db_model

    def create_dynamic_class(self, class_name, base_classes, class_attributes):
        dynamic_class = type(class_name, base_classes, class_attributes)
        return dynamic_class


