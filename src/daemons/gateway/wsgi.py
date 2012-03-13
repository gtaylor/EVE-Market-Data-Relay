import csv
from StringIO import StringIO
from bottle import route, run, request, post

@post('/api/upload/')
def index():
    print "FORMS", request.forms.items()

    log = request.forms.log
    log_buf = StringIO(log)
    for row in csv.reader(log_buf, delimiter=','):
        order_id, \
        buy_sell, \
        solar_system_id, \
        station_id, \
        price, \
        vol_entered,\
        vol_remaining, \
        min_volume, \
        order_issuedate, \
        order_duration, \
        order_range = row

    upload_type = request.forms.upload_type
    region_id = request.forms.region_id

run(host='localhost', port=8080)