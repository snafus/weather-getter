from influxdb import InfluxDBClient
from contextlib import contextmanager

@contextmanager
def get_client(**kwargs):
    """ return the client for influxdb.

        params is a dict containing keys:
        'host' - hostname
        'port' - port

        Only simple non-username, non-ssl is implemented sofar
        Uses the @contextmanager to allow the with statement
    """
    client = InfluxDBClient(host=kwargs['host'], port=kwargs['port'])
    yield client
    client.close()



def initialise_db(client, dbname):
    """Create the db, if not existing, and switch to that database
    """
    if dbname in [x['name'] for x in client.get_list_database()]:
        #db already exists
        pass
    else:
        client.create_database(dbname)
    client.switch_database(dbname)
    return client

def insert_data(client,data):
    """ Insert data into the client db
          arguments:
            client:  the db client
            data  :  list of points, constructed as:
        example point:
               {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-28T8:01:00Z",
        "fields": {
            "duration": 127
        }
    },
    """
    return client.write_points(points=data)


def query_data(client,query):
    """ query the db; no checking of query is performed
    """
    return client.query(query)
