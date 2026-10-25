import os

from dotenv import load_dotenv, find_dotenv
from supabase import create_client, Client

load_dotenv(find_dotenv())

supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_ANON_KEY"])
