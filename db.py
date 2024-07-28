from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Initialize SQLAlchemy without binding it to a specific Flask app
db = SQLAlchemy()

# Configure SQLAlchemy for the MIDOG++ database
midog_engine = create_engine('sqlite:///MIDOG++.sqlite')
MIDOGSession = sessionmaker(bind=midog_engine)
MIDOGBase = declarative_base()

# Define the ModelResult model for the main database
class ModelResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_coordinate = db.Column(db.Float, nullable=False)
    y_coordinate = db.Column(db.Float, nullable=False)
    label = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    model_version = db.Column(db.String(50), nullable=False)

# Define a model for the MIDOG++ database
class MIDOGResult(MIDOGBase):
    __tablename__ = 'midog_results'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.String(50), nullable=False)
    x_coordinate = db.Column(db.Float, nullable=False)
    y_coordinate = db.Column(db.Float, nullable=False)
    classification = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    MIDOGBase.metadata.create_all(midog_engine)

def get_midog_session():
    return MIDOGSession()

def add_model_result(x, y, label, model_version):
    new_result = ModelResult(x_coordinate=x, y_coordinate=y, 
                             label=label, model_version=model_version)
    db.session.add(new_result)
    db.session.commit()

def add_midog_result(image_id, x, y, classification, confidence):
    midog_session = MIDOGSession()
    new_midog_result = MIDOGResult(image_id=image_id, x_coordinate=x, 
                                   y_coordinate=y, classification=classification, 
                                   confidence=confidence)
    midog_session.add(new_midog_result)
    midog_session.commit()
    midog_session.close()

def get_all_model_results():
    return ModelResult.query.all()

def get_all_midog_results():
    midog_session = MIDOGSession()
    results = midog_session.query(MIDOGResult).all()
    midog_session.close()
    return results

def get_midog_results_by_image(image_id):
    midog_session = MIDOGSession()
    results = midog_session.query(MIDOGResult).filter_by(image_id=image_id).all()
    midog_session.close()
    return results