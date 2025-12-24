from datetime import datetime
import zmq, json, psycopg2

conn = psycopg2.connect(dbname="telephony_bd", host="localhost", user="postgres", password="vova100305", port="5432")
cursor = conn.cursor()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:2222")

while True:
    try:
        message = socket.recv()
        data = {k.lower(): v for k, v in json.loads(message.decode()).items()}
        print(f"[SERVER] telephony received: {data}")
        t = data.get('time')
        try:
            formatted_time = datetime.strptime(t, "%d-%m-%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S") if t else None
        except:
            formatted_time = None
        cursor.execute("INSERT INTO user_equipment (formatted_time, latitude, longitude, mcc, mnc, pci, rsrp, rsrq, rssi, rssnr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                       (formatted_time, 
                        data.get('latitude'), 
                        data.get('longitude'), 
                        data.get('mcc'), 
                        data.get('mnc'), 
                        data.get('pci'), 
                        data.get('rsrp'), 
                        data.get('rsrq'), 
                        data.get('rssi'), 
                        data.get('rssnr')))
        conn.commit()
        socket.send(b"OK")
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"[ERROR] {e}")
        conn.rollback()
        socket.send(b"ERR")

socket.close()
context.term()
cursor.close()
conn.close()
