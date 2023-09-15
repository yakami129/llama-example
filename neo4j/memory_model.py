from neomodel import StructuredNode, StringProperty, IntegerProperty, Relationship

class User(StructuredNode):
    userID = StringProperty(unique_index=True)
    name = StringProperty()
    tags = StringProperty(index=True)
    interested_in = Relationship('Interest', 'INTERESTED_IN')
    attended_event = Relationship('Event', 'ATTENDED_EVENT')

class Interest(StructuredNode):
    interestID = StringProperty(unique_index=True)
    name = StringProperty()
    type = StringProperty()

class Event(StructuredNode):
    eventID = StringProperty(unique_index=True)
    name = StringProperty()
    time = StringProperty()
    location = StringProperty()
    description = StringProperty()

class Conversation(StructuredNode):
    conversationID = StringProperty(unique_index=True)
    content = StringProperty()
    time = StringProperty()
    referred_to = Relationship('Interest', 'REFER_TO')
    chatted_to = Relationship('Event', 'CHAT_TO')
