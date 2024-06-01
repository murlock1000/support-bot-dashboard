from __future__ import annotations
from typing import TYPE_CHECKING

import json
import logging
from dataclasses import asdict
from typing import Optional, List
# noinspection PyPackageRequirements
from nio import MegolmEvent

if TYPE_CHECKING:
    from support_bot.models.Repositories.Repositories import Repositories

logger = logging.getLogger(__name__)

class Storage(object):
    def __init__(self, database_config):
        """Connect to the database

        Runs an initial setup or migrations depending on whether a database file has already
        been created

        Args:
            database_config: a dictionary containing the following keys:
                * type: A string, one of "sqlite" or "postgres"
                * connection_string: A string, featuring a connection string that
                    be fed to each respective db library's `connect` method
        """
        self.conn = self._get_database_connection(
            database_config["type"], database_config["connection_string"]
        )
        self.cursor = self.conn.cursor()
        self.db_type = database_config["type"]

        logger.info(f"Database connection of type '{self.db_type}' complete")

    def set_repositories(self, repositories: Repositories):
        self.repositories:Repositories = repositories

    @staticmethod
    def _get_database_connection(database_type: str, connection_string: str):
        if database_type == "sqlite":
            import sqlite3

            # Initialize a connection to the database, with autocommit on
            return sqlite3.connect(connection_string, isolation_level=None)
        elif database_type == "postgres":
            # noinspection PyUnresolvedReferences
            import psycopg2

            conn = psycopg2.connect(connection_string)

            # Autocommit on
            conn.set_isolation_level(0)

            return conn

    def _execute(self, *args):
        """A wrapper around cursor.execute that transforms placeholder ?'s to %s for postgres
        """
        if self.db_type == "postgres":
            self.cursor.execute(args[0].replace("?", "%s"), *args[1:])
        else:
            self.cursor.execute(*args)

    def get_encrypted_events(self, session_id: str) -> List:
        self._execute("""
            select id, device_id, room_id, session_id, event, user_id from encrypted_events where session_id = ?;
        """, (session_id,))
        events = self.cursor.fetchall()
        return [
            {
                "id": row[0],
                "device_id": row[1],
                "room_id": row[2],
                "session_id": row[3],
                "event": row[4],
                "user_id": row[5],
            } for row in events
        ]

    def get_encrypted_events_for_user(self, user_id: str) -> List:
        self._execute("""
            select id, device_id, room_id, session_id, event, user_id from encrypted_events where user_id = ?;
        """, (user_id,))
        events = self.cursor.fetchall()
        return [
            {
                "id": row[0],
                "device_id": row[1],
                "room_id": row[2],
                "session_id": row[3],
                "event": row[4],
                "user_id": row[5],
            } for row in events
        ]

    def get_message_by_management_event_id(self, management_event_id: str) -> Optional[dict]:
        self._execute("SELECT room_id, event_id FROM messages where management_event_id = ?", (management_event_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "room_id": row[0],
                "event_id": row[1],
            }

    def remove_encrypted_event(self, event_id: str):
        self._execute("""
            delete from encrypted_events where event_id = ?;
        """, (event_id,))

    def store_encrypted_event(self, event: MegolmEvent):
        try:
            event_dict = asdict(event)
            event_json = json.dumps(event_dict)
            self._execute("""
                insert into encrypted_events
                    (device_id, event_id, room_id, session_id, event, user_id) values
                    (?, ?, ?, ?, ?, ?)
            """, (event.device_id, event.event_id, event.room_id, event.session_id, event_json, event.sender))
        except Exception as ex:
            logger.error("Failed to store encrypted event %s: %s" % (event.event_id, ex))

    def store_message(self, event_id: str, management_event_id: str, room_id: str):
        self._execute("""
            insert into messages (event_id, management_event_id, room_id) values (?, ?, ?)
        """, (event_id, management_event_id, room_id))
