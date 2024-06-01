import os
from django.apps import AppConfig
from support_lib.config import Config
from support_lib.storage import Storage
from support_bot.models.Repositories.Repositories import Repositories
from django.conf import settings

import grpc

store: Storage = None
config: Config = None
channel: grpc.Channel

def _load_credential_from_file(filepath):
    with open(filepath, "rb") as f:
        return f.read()

class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"
    
    def ready(self):
        global config, store, channel
        config = Config(settings.SUPPORT_BOT_CONFIG_PATH)
        
        # Configure the database
        store = Storage(config.database)

        # Initialise global model repositories:
        repositories = Repositories(store)
        store.set_repositories(repositories)
        
        # Initialize grpc client channel
        root_crt = _load_credential_from_file(settings.ROOT_CERTIFICATE_PATH)
        
        channel_credential = grpc.ssl_channel_credentials(root_crt)
        
        channel = grpc.secure_channel(f"{settings.GRPC_SERVER_ADDR}:{settings.GRPC_SERVER_PORT}", channel_credential)
