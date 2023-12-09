from sqlalchemy.types import Integer, String, LargeBinary, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column


Base = declarative_base()


class DialogRecord(Base):
    __tablename__ = 'dialogs'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    timestamp = Column(DateTime, default=func.current_timestamp(),
                       nullable=False)
    status = Column(String)
    audio2text = Column(String)
    text2advice = Column(String)
    raw_audio = Column(LargeBinary)
    advice_audio = Column(LargeBinary)
    version = Column(BigInteger, nullable=False)
    # for optimistic lock
    __mapper_args__ = {'version_id_col': version}
#    version = Column(Integer, default=0, server_default='0', onupdate=1)
