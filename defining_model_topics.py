from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# 定义 Topic 类
class Topics(Base):
    __tablename__ = 'topics'

    topic_id = Column(Integer, primary_key=True)
    op_id = Column(String(20))
    topic_header = Column(Text)
    topic_content = Column(Text)
    question_time = Column(DateTime)
    number_of_clicks = Column(Integer)
    number_of_replies = Column(Integer)
    last_reply_time = Column(DateTime)
    up_vote_topic = Column(Integer)
    down_vote_topic = Column(Integer)
    topic_category = Column(String(20))
    tag_1 = Column(String(20))
    tag_2 = Column(String(20))
    tag_3 = Column(String(20))
    tag_4 = Column(String(20))

    def __repr__(self):
        return f"<Topics(topic_id={self.topic_id}, op_id='{self.op_id}', topic_header='{self.topic_header[:10]}...', topic_content='{self.topic_content[:20]}...', question_time='{self.question_time}', number_of_clicks={self.number_of_clicks}, number_of_replies={self.number_of_replies}, last_reply_time='{self.last_reply_time}', up_vote_topic={self.up_vote_topic}, down_vote_topic={self.down_vote_topic}, topic_category='{self.topic_category}', tag_1='{self.tag_1}', tag_2='{self.tag_2}', tag_3='{self.tag_3}', tag_4='{self.tag_4}')>"
