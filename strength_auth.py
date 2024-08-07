import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from strength_functions import *
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import base64
from io import BytesIO
import sqlite3


# Database setup
DATABASE_URL = "sqlite:///./lifts.db"
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

# Lift data model
class Lift(Base):
    __tablename__ = 'lifts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    lift_type = Column(String)
    weight = Column(Float)
    reps = Column(Integer)
    time = Column(Float)
    timestamp = Column(String)

def add_timestamp_column():
    conn = sqlite3.connect('lifts.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE lifts ADD COLUMN timestamp TEXT")
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    conn.close()




# Create database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# User authentication
def authenticate_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username, User.password == password).first()
    db.close()
    return user

# User registration
def register_user(username, password):
    db = SessionLocal()
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.close()

# Load user-specific lift data
def load_user_data(user_id):
    db = SessionLocal()
    lifts = db.query(Lift).filter(Lift.user_id == user_id).all()
    db.close()
    if lifts:
        data = pd.DataFrame([{
            'Lift': lift.lift_type,
            'Weight': lift.weight,
            'Reps': lift.reps,
            'Time': lift.time,
            'Timestamp': lift.timestamp
        } for lift in lifts])
    else:
        data = pd.DataFrame(columns=['Lift', 'Weight', 'Reps', 'Time', 'Timestamp'])
    return data
