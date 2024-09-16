from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Agents(db.Model):
    __tablename__ = "agentname"

    name_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone =  db.Column(db.String, nullable=False)
    pollingunit_uniqueid = db.Column(db.Integer)

class AnnouncedPollingUnitResults(db.Model):
    __tablename__ = "announced_pu_results"

    result_id = db.Column(db.Integer, primary_key=True, nullable=False)
    polling_unit_uniqueid = db.Column(db.String(50), nullable=False)
    party_abbreviation = db.Column(db.String(4), nullable=False)
    party_score = db.Column(db.Integer, nullable=False)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_ip_address = db.Column(db.String(50), nullable=False)
    
class LgaScores(db.Model):
    __tablename__ = "announced_lga_results"
   
    result_id = db.Column(db.Integer, primary_key=True)
    lga_name = db.Column(db.String(50), nullable=False)
    party_abbreviation = db.Column(db.String(4), nullable=False)
    party_score = db.Column(db.Integer, nullable=False)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    user_ip_address = db.Column(db.String(50), nullable=False)



