# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# # TODO: Configure data base
# #db_url = {'drivername':'sqlite'}

# #_cwd = dirname(abspath(__file__))
# #db_filename = "flask-contacts.db"
# #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, db_filename)

# engine     = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
# DBSession  = sessionmaker(autocommit=False,autoflush=False,bind=engine)
# db_session = scoped_session(DBSession)
# Base       = declarative_base()
# Base.query = db_session.query_property()

# def init_db():
#     import models
#     Base.metadata.create_all(bind=engine)

