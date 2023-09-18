from django.apps import AppConfig
from support_lib.config import Config
from support_lib.storage import Storage
from middleman.models.Repositories.Repositories import Repositories
from django.conf import settings

store: Storage = None
config: Config = None

class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"
    
    def ready(self):
        global config, store
        config = Config(settings.SUPPORT_BOT_CONFIG_PATH)
        
        # Configure the database
        store = Storage(config.database)

        # Initialise global model repositories:
        repositories = Repositories(store)
        store.set_repositories(repositories)
