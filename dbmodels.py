from sqlalchemy.types import Integer, String, LargeBinary, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column
import uuid


Base = declarative_base()


class DialogRecord(Base):
    class Status:
        INIT = "INIT"
        AUDIO2TEXT_START = "AUDIO2TEXT_START"
        AUDIO2TEXT_NOW = "AUDIO2TEXT_NOW"
        AUDIO2TEXT_END = "AUDIO2TEXT_END"
        TEXT2ADVICE_START = "TEXT2ADVICE_START"
        TEXT2ADVICE_NOW = "TEXT2ADVICE_NOW"
        TEXT2ADVICE_END = "TEXT2ADVICE_END"

    __tablename__ = 'dialogs'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    timestamp = Column(DateTime, default=func.current_timestamp(),
                       nullable=False)
    status = Column(String)
    audio2text = Column(String)
    # advice only
    text2advice = Column(String)
    # full of response(prompt+advice)
    text2advice_full = Column(String)
    raw_audio = Column(LargeBinary)
    advice_audio = Column(LargeBinary)
    version = Column(BigInteger, nullable=False)
    # for optimistic lock
    __mapper_args__ = {'version_id_col': version}
#    version = Column(Integer, default=0, server_default='0', onupdate=1)

    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self.status = DialogRecord.Status.INIT
