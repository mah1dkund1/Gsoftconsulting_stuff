from models import LogEntry
    
class FileParser:
        def __init__(self, filepath):
            self.filepath = filepath
            
        
        def parse(self):
            
            return LogEntry("2026-11-05 17:00", "ERROR", "Connection timeout")