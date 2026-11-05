#below is some basic code for classes objects and constructors

class LogEntry:
    
    def __init__(self , timestamp , level , message):
        
        self.timestamp = timestamp
        self.level = level
        self.message = message
        
    
    def display(self):
        print(f"[{self.level}] {self.timestamp}: {self.message}")
        
    
entry = LogEntry("2026-11-05 , 17:12" , "sUcESSFULL" , "working correctly")

entry.display()
        
    