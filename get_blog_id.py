from googleapiclient.discovery import build
import pickle

with open('token.pkl', 'rb') as token:
    creds = pickle.load(token)

service = build('blogger', 'v3', credentials=creds)

blogs = service.blogs().listByUser(userId='self').execute()

print(blogs)