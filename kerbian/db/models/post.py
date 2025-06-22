from kerbian.db.orm import Model, IntegerField, StringField, ForeignKey, ManyToManyField
from kerbian.db.models.user import User

class Post(Model):
    id = IntegerField(primary_key=True)
    title = StringField()
    author = ForeignKey(User)
    tags = ManyToManyField('Tag')

class Tag(Model):
    id = IntegerField(primary_key=True)
    name = StringField()