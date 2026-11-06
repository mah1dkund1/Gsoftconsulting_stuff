from parsers import FileParser

def main():
    
    print ("starting log analysis CLI...")
    
    parser = FileParser("/logs/app.log")
    entry = parser.parse()
    
    
    print(entry)
    
    if __name__ == "__main__":
        
        main()