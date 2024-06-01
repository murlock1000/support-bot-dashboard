import logging
import os
import re
import sys
from typing import Any, List

import yaml

from support_bot.errors import ConfigError

# Prevent debug messages from peewee lib
logger = logging.getLogger()
logging.getLogger("peewee").setLevel(logging.INFO)
# Prevent info messages from charset_normalizer which seems to output
# lots of weird log lines about probing the chaos if Synapse goes away for a sec
logging.getLogger("charset_normalizer").setLevel(logging.WARNING)


class Config(object):
    def __init__(self, filepath):
        """
        Args:
            filepath (str): Path to config file
        """
        if not os.path.isfile(filepath):
            raise ConfigError(f"Config file '{filepath}' does not exist")

        # Load in the config file at the given filepath
        with open(filepath) as file_stream:
            self.config = yaml.safe_load(file_stream.read())

        # Logging setup
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s [%(levelname)s] %(message)s"
        )

        log_level = self._get_cfg(["logging", "level"], default="INFO")
        logger.setLevel(log_level)

        file_logging_enabled = self._get_cfg(
            ["logging", "file_logging", "enabled"], default=False
        )
        file_logging_filepath = self._get_cfg(
            ["logging", "file_logging", "filepath"], default="bot.log"
        )
        if file_logging_enabled:
            handler = logging.FileHandler(file_logging_filepath)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        console_logging_enabled = self._get_cfg(
            ["logging", "console_logging", "enabled"], default=True
        )
        if console_logging_enabled:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        # Database setup
        database_path = self._get_cfg(["storage", "database"], required=True)

        # Support both SQLite and Postgres backends
        # Determine which one the user intends
        sqlite_scheme = "sqlite://"
        postgres_scheme = "postgres://"
        if database_path.startswith(sqlite_scheme):
            self.database = {
                "type": "sqlite",
                "connection_string": database_path[len(sqlite_scheme):],
            }
        elif database_path.startswith(postgres_scheme):
            self.database = {"type": "postgres", "connection_string": database_path}
        else:
            raise ConfigError("Invalid connection string for storage.database")

        # Matrix bot account setup
        self.user_id = self._get_cfg(["matrix", "user_id"], required=True)
        if not re.match("@.*:.*", self.user_id):
            raise ConfigError("matrix.user_id must be in the form @name:domain")
        self.user_localpart = self.user_id.split(":")[0][1:]

        self.homeserver_url = self._get_cfg(["matrix", "homeserver_url"], required=True)

        self.command_prefix = self._get_cfg(["command_prefix"], default="!c") + " "

        # Matrix logging
        matrix_logging_enabled = self._get_cfg(["logging", "matrix_logging", "enabled"], default=False)
        self.matrix_logging_room = None
        if matrix_logging_enabled:
                self.matrix_logging_room = self._get_cfg(["logging", "matrix_logging", "room"], required=True)

        # Middleman specific config
        self.management_room = self._get_cfg(["middleman", "management_room"], required=True)
        self.management_room_id = self.management_room if self.management_room.startswith("!") else None
        self.anonymise_senders = self._get_cfg(["middleman", "anonymise_senders"], required=False, default=False)
        self.mention_only_rooms = self._get_cfg(["middleman", "mention_only_rooms"], required=False, default=[])
        self.mention_only_always_for_named = self._get_cfg(
            ["middleman", "mention_only_always_for_named"], required=False, default=False,
        )
        self.confirm_reaction = self._get_cfg(["middleman", "confirm_reaction", "enabled"], required=False, default=False)
        self.confirm_reaction_success = self._get_cfg(["middleman", "confirm_reaction", "success"], required=False, default="✔️")
        self.confirm_reaction_fail = self._get_cfg(["middleman", "confirm_reaction", "fail"], required=False, default="❗")
        self.relay_management_media = self._get_cfg(["middleman", "relay_management_media"], required=False, default=False)

    def _get_cfg(
        self, path: List[str], default: Any = None, required: bool = True,
    ) -> Any:
        """Get a config option from a path and option name, specifying whether it is
        required.

        Raises:
            ConfigError: If required is specified and the object is not found
                (and there is no default value provided), this error will be raised
        """
        # Shift through the config until we reach our option
        config = self.config
        for name in path:
            config = config.get(name)

            # If at any point we don't get our expected option...
            if config is None:
                # Raise an error if it was required
                if required and not default:
                    raise ConfigError(f"Config option {'.'.join(path)} is required")

                # or return the default value
                return default

        # We found the option. Return it
        return config
