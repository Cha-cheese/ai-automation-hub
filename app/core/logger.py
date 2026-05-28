import datetime

def log(event, data):
    print(f"[LOG {datetime.datetime.now()}] {event}: {data}")