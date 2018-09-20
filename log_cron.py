import time
import sys
from datetime import datetime
import Adafruit_DHT
from influxdb import InfluxDBClient

'''
With code & influence from:
https://www.modmypi.com/blog/am2302-temphumidity-sensor
https://www.definit.co.uk/2018/07/monitoring-temperature-and-humidity-with-a-raspberry-pi-3-dht22-sensor-influxdb-and-grafana/
https://github.com/adafruit/Adafruit_Python_DHT

'''
# Configure InfluxDB connection variables
host = "localhost" # My Ubuntu NUC
port = 8086 # default port
user = "admin" # the user/password created for the pi, with write access
password = "admin" 
dbname = "logger" # the database we created earlier
interval = 5 # Sample period in seconds

# Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)

# Enter the sensor details
sensor = Adafruit_DHT.AM2302
sensor_gpio = 4

# think of measurement as a SQL table, it's not...but...
measurement = "AM2302"

# location will be used as a grouping tag later
location = "cork"


# Read the sensor using the configured driver and gpio
humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

# Un-comment the line below to convert the temperature to Fahrenheit.
temperature = temperature * 9/5.0 + 32

# Print for debugging, uncomment the below line
print("[%s] Temp: %s, Humidity: %s" % (current_time, temperature, humidity)) 


# Create the JSON data structure
data = [
{
    "measurement": measurement,
        "tags": {
        "location": location,
        },
        "time": current_time,
        "fields": {
        "temperature" : temperature,
        "humidity": humidity
        }
    }
]
# Send the JSON data to InfluxDB
client.write_points(data)
# Wait until it's time to query again...
#time.sleep(interval)
 
