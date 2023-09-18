import logging
from django.apps import AppConfig

from middleman.models.Repositories.TicketRepository import TicketRepository
from support_lib.config import Config
from support_lib.storage import Storage
from middleman.models.Repositories.Repositories import Repositories
from django.conf import settings

class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"
    
    def ready(self):
        self.config = Config(settings.SUPPORT_BOT_CONFIG_PATH)
        
        # Configure the database
        self.store = Storage(self.config.database)

        # Initialise global model repositories:
        repositories = Repositories(self.store)
        self.store.set_repositories(repositories)
        
        ticket_rep: TicketRepository = self.store.repositories.ticketRep
        
        tickets = ticket_rep.get_open_tickets()
        logging.warning("Tickets: %s", tickets)
