#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Boolean, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database, drop_database
import os

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'freshdesk.db'))
if database_exists(engine.url):
    drop_database(engine.url)
else:
    create_database(engine.url)

Base = declarative_base()

class Contacts(Base):
    __tablename__='Contacts'
    id=Column(Integer, primary_key=True)
    name=Column(String(60))
    active=Column(Boolean)
    address=Column(String(60))
    company_id=Column(Integer)
    email=Column(String(60))
    job_title=Column(String(60))
    language=Column(String(10))
    description=Column(Text)
    phone=Column(String(20))
    mobile=Column(String(20))

class Companies(Base):
    __tablename__='Companies'
    id=Column(Integer, primary_key=True)
    name=Column(String(60))
    description=Column(Text)
    domains=Column(String(60))

class Groups(Base):
    __tablename__='Groups'
    id=Column(Integer, primary_key=True)
    name=Column(String(60))
    description=Column(Text)

class Tickets(Base):
    __tablename__='Tickets'
    id=Column(Integer, primary_key=True)
    group_id=Column(Integer)
    requester_id=Column(Integer)
    status=Column(Integer)
    subject=Column(String(200))
    company_id=Column(Integer)
    description_text=Column(Text)
    nr_produktu=Column(String(60))
    nr_seryjny=Column(String(60))
    created_at=Column(String(60))
    updated_at=Column(String(60))

class Conversations(Base):
    __tablename__='Conversations'
    id=Column(Integer, primary_key=True)
    body_text=Column(Text)
    user_id=Column(Integer)
    ticket_id=Column(Integer)

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
