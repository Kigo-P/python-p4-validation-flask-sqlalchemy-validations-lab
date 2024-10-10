from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    # validating name
    @validates("name")
    def validate_name(self, key, name):
        existing_author = Author.query.filter_by(name=name).first()
        if not name:
            raise ValueError("The author must have a name ")
        elif existing_author is not None:
            raise ValueError("The author must have a unique name")
        else:
            return name

    # validating authors phone number to be exactly 10 digits
    @validates("phone_number")
    def validates_phone_number(self, key, value):
        if not value or len(value) != 10 or not value.isdigit():
            raise ValueError("The phone number must have 10 digits")
        else:
            return value


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    # validating post content to be at least 250 characters
    @validates("content")
    def validates_content(self, key, value):
        if not value or len(value) < 250:
            raise ValueError("The content must have atleast 250 characters")
        else:
            return value

    # validating post summary to be a maximum 250 characters
    @validates("summary")
    def validates_summary(self, key, value):
        if not value or len(value) > 250:
            raise ValueError("The summary must have a maximum 250 characters")
        else:
            return value

    category_list = ["Fiction","Non-Fiction"]
    # validating post category to be eiter fiction or non fiction
    @validates("category")
    def validates_category(self, key, value):
        
        if value not in self.category_list:
            raise ValueError("The category must be either Fiction or Non-fiction")
        else:
            return value

     # Validating post title to contain clickbait phrases
    @validates("title")
    def validates_title(self, key, value):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError("The title must contain one of the clickbait phrases: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
        return value



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
