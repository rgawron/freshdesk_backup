#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
from models import Contacts, Companies, Groups, Tickets, Conversations
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

FRESHDESK = 'domain.freshdesk.com'
API = 'api_key' 
basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'freshdesk.db'))


def get_contacts():
    r = requests.get("https://" + FRESHDESK + "/api/v2/contacts", auth=(API, 'X'))
    if r.status_code == 200:
        parsed = json.loads(str(r.text))
        return parsed
    else:
        print("Error: Getting contacts")
        print("Status Code : " + r.status_code)
        return 0  # Error


def get_companies():
    r = requests.get("https://" + FRESHDESK + "/api/v2/companies", auth=(API, 'X'))
    if r.status_code == 200:
        parsed = json.loads(str(r.text))
        return parsed
    else:
        print("Error: Getting companies")
        print("Status Code : " + r.status_code)
        return 0  # Error


def get_groups():
    r = requests.get("https://" + FRESHDESK + "/api/v2/groups", auth=(API, 'X'))
    if r.status_code == 200:
        parsed = json.loads(str(r.text))
        return parsed  # OK
    else:
        print("Error: Getting groups")
        print("Status Code : " + r.status_code)
        return 1  # Error


def get_tickets():
    r = requests.get("https://" + FRESHDESK + "/api/v2/tickets", auth=(API, 'X'))
    if r.status_code == 200:
        parsed = json.loads(str(r.text))
        return parsed  # OK
    else:
        print("Error: Getting tickets")
        print("Status Code : " + r.status_code)
        return 1  # Error

def put_contacts(contacts):
    if contacts != False:
        session = sessionmaker(bind=engine)
        s = session()
        for i in range(len(contacts)):
            c = Contacts(id=contacts[i]['id'], name=contacts[i]['name'], active=contacts[i]['active'],
                         address=contacts[i]['address'], company_id=contacts[i]['company_id'],
                         email=contacts[i]['email'], job_title=contacts[i]['job_title'],
                         language=contacts[i]['language'], description=contacts[i]['description'],
                         phone=contacts[i]['phone'], mobile=contacts[i]['mobile'])
            s.add(c)
            s.commit()
            s.close()
        return 0  # OK
    else:
        return 1  # Error


def put_companies(companies):
    if companies != False:
        session = sessionmaker(bind=engine)
        s = session()
        for i in range(len(companies)):
            if not companies[i]['domains']:
                d = ''
            c = Companies(id=companies[i]['id'], name=companies[i]['name'], description=companies[i]['description'],
                          domains=d)
            s.add(c)
            s.commit()
            s.close()
        return 0  # OK
    else:
        return 1  # Error


def put_groups(groups):
    if groups != False:
        session = sessionmaker(bind=engine)
        s = session()
        for i in range(len(groups)):
            c = Groups(id=groups[i]['id'], name=groups[i]['name'], description=groups[i]['description'])
            s.add(c)
            s.commit()
            s.close()
        return 0  # OK
    else:
        return 1  # Error


def put_tickets(tickets):
    if tickets != False:
        session = sessionmaker(bind=engine)
        s = session()
        for i in range(len(tickets)):
            custom = tickets[i]['custom_fields']
            seria = custom['nr_seryjny']
            if seria == None:
                seria = ''
            produkt = custom['nr_produktu']
            if produkt == None:
                produkt = ''
            c = Tickets(id=tickets[i]['id'], group_id=tickets[i]['group_id'], requester_id=tickets[i]['requester_id'],
                       status=tickets[i]['status'], subject=tickets[i]['subject'], company_id=tickets[i]['company_id'],
                       description_text=tickets[i]['description_text'], nr_produktu=produkt, nr_seryjny=seria,
                       created_at=tickets[i]['created_at'], updated_at=tickets[i]['updated_at'])
            s.add(c)
            s.commit()
            s.close()
        return 0  # OK
    else:
        return 1  # Error

def get_conversations():
    session = sessionmaker(bind=engine)
    s = session()
    tickets=s.query(Tickets).all()
    for i in range(len(tickets)):
        r = requests.get("https://" + FRESHDESK + "/api/v2/tickets/"+str(tickets[i].id)+"/conversations", auth=(API, 'X'))
        if r.status_code == 200:
            parsed = json.loads(str(r.text))
            put_conversations(parsed)
        else:
            print("Error: Getting Conversations")
            print("Status Code : " + r.status_code)
            return 1  # Error

def put_conversations(conversations):
    if conversations != False:
        session = sessionmaker(bind=engine)
        s = session()
        for i in range(len(conversations)):
            c = Conversations(id=conversations[i]['id'],body_text=conversations[i]['body_text'],user_id=conversations[i]['user_id'],ticket_id=conversations[i]['ticket_id'])
            s.add(c)
            s.commit()
            s.close()
        return 0  # OK
    else:
        return 1  # Error

put_contacts(get_contacts())
put_companies(get_companies())
put_groups(get_groups())
put_tickets(get_tickets())
get_conversations()
