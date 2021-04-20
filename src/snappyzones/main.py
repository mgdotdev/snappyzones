from .service import Service

def main():
    service = Service()
    service.listen()
    
if __name__ == "__main__":
    main()