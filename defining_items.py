from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

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

    replies = relationship("Replies", order_by="Replies.floor", back_populates="topic")

    def __repr__(self):
        return f"<Topics(topic_id={self.topic_id}, op_id='{self.op_id}', topic_header='{self.topic_header[:10]}...', topic_content='{self.topic_content[:20]}...', question_time='{self.question_time}', number_of_clicks={self.number_of_clicks}, number_of_replies={self.number_of_replies}, last_reply_time='{self.last_reply_time}', up_vote_topic={self.up_vote_topic}, down_vote_topic={self.down_vote_topic}, topic_category='{self.topic_category}', tag_1='{self.tag_1}', tag_2='{self.tag_2}', tag_3='{self.tag_3}', tag_4='{self.tag_4}')>"


class Replies(Base):
    __tablename__ = 'replies'

    reply_id = Column(String(20), primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))
    floor = Column(Integer)
    reply_content = Column(Text)
    reply_time = Column(DateTime)
    number_of_thanks = Column(Integer)
    is_it_op = Column(Boolean)

    # Relationship to Topics
    topic = relationship("Topics", back_populates="replies")

    def __repr__(self):
        return f"<Replies(reply_id='{self.reply_id}', topic_id={self.topic_id}, floor={self.floor}, reply_content='{self.reply_content[:20]}...', reply_time='{self.reply_time}', number_of_thanks={self.number_of_thanks}, is_it_op='{self.is_it_op}')>"


Topics.replies = relationship("Replies", order_by="Replies.floor", back_populates="topic")
