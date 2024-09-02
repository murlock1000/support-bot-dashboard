from dataclasses import asdict, dataclass
from datetime import datetime
from support_bot.models.Repositories.ChatRepository import ChatRepository, ChatStatus

@dataclass
class ChatResult():
    chat_room_id: str
    user_id: str
    status: str
    
    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

class DataChatRepository(ChatRepository):
    
    def __init__(self, chat_rep: ChatRepository):
        self.storage = chat_rep.storage
        
    def get_filtered_chats(self, start_date: datetime, end_date: datetime, status: ChatStatus) -> [ChatResult]:
        if start_date is None or end_date is None:
            if status:
                self.storage._execute("""
                    SELECT chat_room_id, user_id, status FROM Chats
                    WHERE created_at IS null AND status = ?
                """, (status,))
            else:
                self.storage._execute("""
                    SELECT chat_room_id, user_id, status FROM Chats
                    WHERE created_at is null
                """, ())
        else:
            if status:
                self.storage._execute("""
                    SELECT chat_room_id, user_id, status FROM Chats
                    WHERE created_at >= ? AND created_at <= ? AND status = ?
                """, (start_date, end_date, status,))
            else:
                self.storage._execute("""
                    SELECT chat_room_id, user_id, status FROM Chats
                    WHERE created_at >= ? AND created_at <= ?
                """, (start_date, end_date,))

        chats = self.storage.cursor.fetchall()
        return [
            ChatResult(chat[0], chat[1], chat[2]) for chat in chats
        ]
    
    def get_open_chats_of_staff(self, staff_id:str):
        self.storage._execute("""
            SELECT chat_room_id, user_id FROM Chats t JOIN ChatsStaffRelation ts ON t.chat_room_id=ts.chat_id WHERE status=? AND staff_id=?
        """, (ChatStatus.OPEN.value, staff_id, ))

        chats = self.storage.cursor.fetchall()
        return [
            {
                'chat_room_id':chat[0],
                'user_id': chat[1],
            } for chat in chats
        ]
        
    def get_filtered_staff_chats(self, start_date: datetime, end_date: datetime, status: ChatStatus, staff_id:str) -> [ChatResult]:
        if status:
            self.storage._execute("""
                SELECT chat_room_id, user_id, status FROM Chats t JOIN ChatsStaffRelation ts ON t.chat_room_id=ts.chat_id
                WHERE created_at >= ? AND created_at <= ? AND status = ? AND staff_id=?
            """, (start_date, end_date, status, staff_id,))
        else:
            self.storage._execute("""
                SELECT chat_room_id, user_id, status FROM Chats t JOIN ChatsStaffRelation ts ON t.chat_room_id=ts.chat_id
                WHERE created_at >= ? AND created_at <= ? AND staff_id=?
            """, (start_date, end_date, staff_id,))

        chats = self.storage.cursor.fetchall()
        return [
            ChatResult(chat[0], chat[1], chat[2]) for chat in chats
        ]

    def get_chat_count(self, status:ChatStatus) -> int:
        self.storage._execute("""
            SELECT COUNT(chat_room_id) FROM Chats
            WHERE status = ?;
        """, (status.value,))
        count = self.storage.cursor.fetchone()
        return count[0] if count else 0
    
    def get_staff_chat_count(self, status:ChatStatus, staff_id:str) -> int:
        self.storage._execute("""
            SELECT COUNT(t.chat_room_id) FROM Chats t JOIN ChatsStaffRelation ts ON t.chat_room_id=ts.chat_id
            WHERE t.status = ? AND ts.staff_id = ?;
        """, (status.value, staff_id,))
        count = self.storage.cursor.fetchone()
        return count[0] if count else 0
    
    def get_chat_count_in_interval(self, start_date:datetime, end_date:datetime, status:ChatStatus) -> int:
        self.storage._execute("""
            SELECT COUNT(chat_room_id) FROM Chats
            WHERE created_at >= ? AND created_at <= ? AND status = ?;
        """, (start_date, end_date, status.value,))
        count = self.storage.cursor.fetchone()
        return count[0] if count else 0
    
    def get_opened_chats_by_month(self, start_date:datetime, end_date:datetime) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('month', closed_at) AS month, COUNT(chat_room_id) FROM Chats
            WHERE created_at >= ? AND created_at <= ?
            GROUP BY month
            ORDER BY month;
        """, (start_date, end_date,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_closed_chats_by_month(self, start_date:datetime, end_date:datetime) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('month', closed_at) AS month, COUNT(chat_room_id) FROM Chats
            WHERE closed_at >= ? AND closed_at <= ? AND closed_at IS NOT NULL
            GROUP BY month
            ORDER BY month;
        """, (start_date, end_date,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_staff_closed_chats_by_month(self, start_date:datetime, end_date:datetime, staff_id:str) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('month', closed_at) AS month, COUNT(chat_room_id) FROM Chats t JOIN ChatsStaffRelation ts ON t.chat_room_id=ts.chat_id
            WHERE closed_at >= ? AND closed_at <= ? AND closed_at IS NOT NULL AND staff_id = ?
            GROUP BY month
            ORDER BY month;
        """, (start_date, end_date, staff_id,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_staff_opened_chats_by_month(self, start_date:datetime, end_date:datetime, staff_id:str) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('month', closed_at) AS month, COUNT(chat_room_id) FROM Chats t JOIN ChatsStaffRelation ts ON t.chat_room_id=ts.chat_id
            WHERE created_at >= ? AND created_at <= ? AND staff_id = ?
            GROUP BY month
            ORDER BY month;
        """, (start_date, end_date, staff_id,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_opened_chats_by_day(self, start_date:datetime, end_date:datetime) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('day', closed_at) AS day, COUNT(chat_room_id) FROM Chats
            WHERE created_at >= ? AND created_at <= ?
            GROUP BY day
            ORDER BY day;
        """, (start_date, end_date,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_staff_opened_chats_by_day(self, start_date:datetime, end_date:datetime, staff_id:str) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('day', closed_at) AS day, COUNT(chat_room_id) FROM Chats t JOIN ChatsStaffRelation ts ON t.chat_room_id=ts.chat_id
            WHERE created_at >= ? AND created_at <= ? AND staff_id = ?
            GROUP BY day
            ORDER BY day;
        """, (start_date, end_date, staff_id,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_staff_closed_chats_by_day(self, start_date:datetime, end_date:datetime, staff_id:str) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('day', closed_at) AS day, COUNT(chat_room_id) FROM Chats t JOIN ChatsStaffRelation ts ON t.chat_room_id=ts.chat_id
            WHERE closed_at >= ? AND closed_at <= ? AND closed_at IS NOT NULL AND staff_id = ?
            GROUP BY day
            ORDER BY day;
        """, (start_date, end_date, staff_id,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_homepage_chats(self):
        self.storage._execute("""
            SELECT chat_room_id, user_id, created_at FROM Chats WHERE status=?
        """, (ChatStatus.OPEN.value,))

        chats = self.storage.cursor.fetchall()
        return [
            {
                'chat_room_id':chat[0],
                'user_id': chat[1],
                'created_at' : chat[2],
            } for chat in chats
        ]
        
    def get_staff_info_chats(self, staff_id:str):
        self.storage._execute("""
            SELECT chat_room_id, user_id, created_at FROM Chats t JOIN ChatsStaffRelation ts ON t.chat_room_id=ts.chat_id
            WHERE status=? AND staff_id=?
        """, (ChatStatus.OPEN.value, staff_id,))

        chats = self.storage.cursor.fetchall()
        return [
            {
                'chat_room_id':chat[0],
                'user_id': chat[1],
                'created_at' : chat[2],
            } for chat in chats
        ]