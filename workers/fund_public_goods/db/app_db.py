import os
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions


load_dotenv()

URL_ENV = "NEXT_PUBLIC_SUPABASE_URL"
ANON_KEY_ENV = "NEXT_PUBLIC_SUPABASE_ANON_KEY"
SERV_KEY_ENV = "SUPABASE_SERVICE_ROLE_KEY"

class Env(BaseModel):
    url: str
    anon_key: str
    serv_key: str

def load_env() -> Env:
    url: str | None = os.environ.get(URL_ENV)
    anon_key: str | None = os.environ.get(ANON_KEY_ENV)
    serv_key: str | None = os.environ.get(SERV_KEY_ENV)

    if url is None:
        raise Exception(f"{URL_ENV} is not set")
    if anon_key is None:
        raise Exception(f"{ANON_KEY_ENV} is not set")
    if serv_key is None:
        raise Exception(f"{SERV_KEY_ENV} is not set")

    return Env(
        url=url,
        anon_key=anon_key,
        serv_key=serv_key
    )

def create(options: ClientOptions = ClientOptions()) -> Client:
    env = load_env()
    return create_client(env.url, env.anon_key, options)

def create_admin(schema: Optional[str] = None) -> Client:
    env = load_env()

    if schema:
        options = ClientOptions(schema=schema)
        return create_client(env.url, env.serv_key, options)
    else:
        return create_client(env.url, env.serv_key)
