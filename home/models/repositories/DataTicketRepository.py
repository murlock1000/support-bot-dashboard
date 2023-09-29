from datetime import datetime
from middleman.models.Repositories.TicketRepository import TicketRepository, TicketStatus
    
class DataTicketRepository(TicketRepository):
    
    def __init__(self, ticket_rep: TicketRepository):
        self.storage = ticket_rep.storage
        
    def get_ticket_count(self, status:TicketStatus) -> int:
        self.storage._execute("""
            SELECT COUNT(id) FROM Tickets
            WHERE status = ?;
        """, (status.value,))
        count = self.storage.cursor.fetchone()
        return count[0] if count else 0
    
    def get_ticket_count_in_interval(self, start_date:datetime, end_date:datetime, status:TicketStatus) -> int:
        self.storage._execute("""
            SELECT COUNT(id) FROM Tickets
            WHERE raised_at >= ? AND raised_at <= ? AND status = ?;
        """, (start_date, end_date, status.value,))
        count = self.storage.cursor.fetchone()
        return count[0] if count else 0
    
    def get_tickets_by_month(self, start_date) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('month', closed_at) AS month, COUNT(id) FROM Tickets
            WHERE raised_at >= ? AND closed_at IS NOT NULL
            GROUP BY month
            ORDER BY month;
        """, (start_date,))
        data = self.storage.cursor.fetchall()
        return data
    
    def get_tickets_by_day(self, start_date) -> [(datetime, int)]:
        self.storage._execute("""
            SELECT DATE_TRUNC('day', closed_at) AS day, COUNT(id) FROM Tickets
            WHERE raised_at >= ? AND closed_at IS NOT NULL
            GROUP BY day
            ORDER BY day;
        """, (start_date,))
        data = self.storage.cursor.fetchall()
        return data