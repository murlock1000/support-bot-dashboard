from dataclasses import asdict, dataclass
from datetime import datetime
from support_bot.models.Repositories.TicketRepository import TicketRepository, TicketStatus

@dataclass
class TicketResult():
    id: int
    user_id: str
    ticket_name: str
    status: str
    
    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

class DataTicketRepository(TicketRepository):
    
    def __init__(self, ticket_rep: TicketRepository):
        self.storage = ticket_rep.storage
        
    def get_filtered_tickets(self, start_date: datetime, end_date: datetime, status: TicketStatus) -> [TicketResult]:
        
        if status:
            self.storage._execute("""
                SELECT id, user_id, ticket_name, status FROM Tickets
                WHERE raised_at >= ? AND raised_at <= ? AND status = ?
            """, (start_date, end_date, status,))
        else:
            self.storage._execute("""
                SELECT id, user_id, ticket_name, status FROM Tickets
                WHERE raised_at >= ? AND raised_at <= ?
            """, (start_date, end_date,))

        tickets = self.storage.cursor.fetchall()
        return [
            TicketResult(ticket[0], ticket[1], ticket[2], ticket[3]) for ticket in tickets
        ]
    
    def get_open_tickets_of_staff(self, staff_id:str):
        self.storage._execute("""
            SELECT id, user_id, ticket_name FROM Tickets t JOIN TicketsStaffRelation ts ON t.id=ts.ticket_id WHERE status=? AND staff_id=?
        """, (TicketStatus.OPEN.value, staff_id, ))

        tickets = self.storage.cursor.fetchall()
        return [
            {
                'id':ticket[0],
                'user_id': ticket[1],
                'ticket_name' : ticket[2]
            } for ticket in tickets
        ]
        
    def get_filtered_staff_tickets(self, start_date: datetime, end_date: datetime, status: TicketStatus, staff_id:str) -> [TicketResult]:
        if status:
            self.storage._execute("""
                SELECT id, user_id, ticket_name, status FROM Tickets t JOIN TicketsStaffRelation ts ON t.id=ts.ticket_id
                WHERE raised_at >= ? AND raised_at <= ? AND status = ? AND staff_id=?
            """, (start_date, end_date, status, staff_id,))
        else:
            self.storage._execute("""
                SELECT id, user_id, ticket_name, status FROM Tickets t JOIN TicketsStaffRelation ts ON t.id=ts.ticket_id
                WHERE raised_at >= ? AND raised_at <= ? AND staff_id=?
            """, (start_date, end_date, staff_id,))

        tickets = self.storage.cursor.fetchall()
        return [
            TicketResult(ticket[0], ticket[1], ticket[2], ticket[3]) for ticket in tickets
        ]

    def get_ticket_count(self, status:TicketStatus) -> int:
        self.storage._execute("""
            SELECT COUNT(id) FROM Tickets
            WHERE status = ?;
        """, (status.value,))
        count = self.storage.cursor.fetchone()
        return count[0] if count else 0
    
    def get_staff_ticket_count(self, status:TicketStatus, staff_id:str) -> int:
        self.storage._execute("""
            SELECT COUNT(t.id) FROM Tickets t JOIN TicketsStaffRelation ts ON t.id=ts.ticket_id
            WHERE t.status = ? AND ts.staff_id = ?;
        """, (status.value, staff_id,))
        count = self.storage.cursor.fetchone()
        return count[0] if count else 0
    
    def get_ticket_count_in_interval(self, start_date:datetime, end_date:datetime, status:TicketStatus) -> int:
        self.storage._execute("""
            SELECT COUNT(id) FROM Tickets
            WHERE raised_at >= ? AND raised_at <= ? AND status = ?;
        """, (start_date, end_date, status.value,))
        count = self.storage.cursor.fetchone()
        return count[0] if count else 0
    
    def get_opened_tickets_by_month(self, start_date:datetime, end_date:datetime) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('month', closed_at) AS month, COUNT(id) FROM Tickets
            WHERE raised_at >= ? AND raised_at <= ?
            GROUP BY month
            ORDER BY month;
        """, (start_date, end_date,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_closed_tickets_by_month(self, start_date:datetime, end_date:datetime) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('month', closed_at) AS month, COUNT(id) FROM Tickets
            WHERE closed_at >= ? AND closed_at <= ? AND closed_at IS NOT NULL
            GROUP BY month
            ORDER BY month;
        """, (start_date, end_date,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_staff_closed_tickets_by_month(self, start_date:datetime, end_date:datetime, staff_id:str) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('month', closed_at) AS month, COUNT(id) FROM Tickets t JOIN TicketsStaffRelation ts ON t.id=ts.ticket_id
            WHERE closed_at >= ? AND closed_at <= ? AND closed_at IS NOT NULL AND staff_id = ?
            GROUP BY month
            ORDER BY month;
        """, (start_date, end_date, staff_id,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_staff_opened_tickets_by_month(self, start_date:datetime, end_date:datetime, staff_id:str) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('month', closed_at) AS month, COUNT(id) FROM Tickets t JOIN TicketsStaffRelation ts ON t.id=ts.ticket_id
            WHERE raised_at >= ? AND raised_at <= ? AND staff_id = ?
            GROUP BY month
            ORDER BY month;
        """, (start_date, end_date, staff_id,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_opened_tickets_by_day(self, start_date:datetime, end_date:datetime) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('day', closed_at) AS day, COUNT(id) FROM Tickets
            WHERE raised_at >= ? AND raised_at <= ?
            GROUP BY day
            ORDER BY day;
        """, (start_date, end_date,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_staff_opened_tickets_by_day(self, start_date:datetime, end_date:datetime, staff_id:str) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('day', closed_at) AS day, COUNT(id) FROM Tickets t JOIN TicketsStaffRelation ts ON t.id=ts.ticket_id
            WHERE raised_at >= ? AND raised_at <= ? AND staff_id = ?
            GROUP BY day
            ORDER BY day;
        """, (start_date, end_date, staff_id,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_staff_closed_tickets_by_day(self, start_date:datetime, end_date:datetime, staff_id:str) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('day', closed_at) AS day, COUNT(id) FROM Tickets t JOIN TicketsStaffRelation ts ON t.id=ts.ticket_id
            WHERE closed_at >= ? AND closed_at <= ? AND closed_at IS NOT NULL AND staff_id = ?
            GROUP BY day
            ORDER BY day;
        """, (start_date, end_date, staff_id,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_homepage_tickets(self):
        self.storage._execute("""
            SELECT id, user_id, ticket_name, raised_at FROM Tickets WHERE status=?
        """, (TicketStatus.OPEN.value,))

        tickets = self.storage.cursor.fetchall()
        return [
            {
                'id':ticket[0],
                'user_id': ticket[1],
                'ticket_name' : ticket[2],
                'raised_at' : ticket[3],
            } for ticket in tickets
        ]
        
    def get_staff_info_tickets(self, staff_id:str):
        self.storage._execute("""
            SELECT id, user_id, ticket_name, raised_at FROM Tickets t JOIN TicketsStaffRelation ts ON t.id=ts.ticket_id
            WHERE status=? AND staff_id=?
        """, (TicketStatus.OPEN.value, staff_id,))

        tickets = self.storage.cursor.fetchall()
        return [
            {
                'id':ticket[0],
                'user_id': ticket[1],
                'ticket_name' : ticket[2],
                'raised_at' : ticket[3],
            } for ticket in tickets
        ]