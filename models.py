from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class School(db.Model):
    __tablename__ = 'schools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    main_link = db.Column(db.String(500), nullable=False)
    grad_link = db.Column(db.String(500), nullable=False)
    dept_link = db.Column(db.String(500), nullable=True)
    recruit_link = db.Column(db.String(500), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'province': self.province,
            'links': {
                'main': self.main_link,
                'grad': self.grad_link,
                'dept': self.dept_link,
                'recruit': self.recruit_link
            }
        }

class SearchResult(db.Model):
    __tablename__ = 'search_results'
    
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    found = db.Column(db.Boolean, default=False)
    error = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(500), nullable=True)
    date = db.Column(db.String(50), nullable=True)
    url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    school = db.relationship('School')
    
    def to_dict(self):
        return {
            'id': self.id,
            'school_id': self.school_id,
            'school_name': self.school.name if self.school else '',
            'found': self.found,
            'error': self.error,
            'title': self.title,
            'date': self.date,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Collection(db.Model):
    __tablename__ = 'collections'
    
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    school = db.relationship('School')