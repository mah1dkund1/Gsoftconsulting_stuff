class SystemTracker:
    def __init__(self):
        self.action_history = []
        self.unique_ips = set()
        
        self.action_counts = {}
        
        self.server_config = ("127.0.0.1", 8080, "production")

    def log_action(self, ip_address: str, action: str):
        self.action_history.append(action)
        
        self.unique_ips.add(ip_address)
        
        self.action_counts[action] = self.action_counts.get(action, 0) + 1

    def get_config_port(self) -> int:
        return self.server_config[1]

if __name__ == "__main__":
    tracker = SystemTracker()
    
    tracker.log_action("192.168.1.1", "LOGIN")
    tracker.log_action("10.0.0.5", "CLICK")
    tracker.log_action("192.168.1.1", "LOGOUT")
    tracker.log_action("10.0.0.5", "CLICK")
    
    print("History:", tracker.action_history) 
    print("Unique IPs:", tracker.unique_ips)  
    print("Counts:", tracker.action_counts)   
    print("Port:", tracker.get_config_port()) 