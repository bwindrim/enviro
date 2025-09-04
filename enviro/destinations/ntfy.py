from enviro import logging
from enviro.constants import UPLOAD_SUCCESS, UPLOAD_FAILED
import urequests
import config

def log_destination():
  logging.info(f"> uploading cached readings to ntfy at: {config.custom_http_url}")

def upload_reading(reading):
  url = config.custom_http_url

  auth = None
  if config.custom_http_username:
    auth = (config.custom_http_username, config.custom_http_password)

  try:
    # get the readings from the JSON dictionary
    readings = reading.get("readings")
    moisture_A = readings.get("moisture_a")
    moisture_B = readings.get("moisture_b")
    moisture_C = readings.get("moisture_c")
    warn = readings.get("alert")
    humidity = readings.get("humidity")
    temperature = readings.get("temperature")
    timestamp = reading.get("timestamp")
    tags = ""
    
    if warn:
        tags = "warning"

    # construct the message string
    msg = f"Moisture A: {moisture_A}, B: {moisture_B}, C: {moisture_C},\nHumidity: {humidity}%, Temperature: {temperature}"
    logging.info(msg)
    # post reading data to http endpoint
    result = urequests.post(url, auth=auth, data=msg.encode("utf-8"),
                            headers={"Title": timestamp, "Tags": tags})
    result.close()

    if result.status_code in [200, 201, 202]:
      return UPLOAD_SUCCESS

    logging.debug(f"  - upload issue ({result.status_code} {result.reason})")
  except Exception as e:
    logging.debug(f"  - an exception occurred when uploading: {e}")

  return UPLOAD_FAILED
