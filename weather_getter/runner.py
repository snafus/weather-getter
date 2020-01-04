import sys
import argparse


import caller,config,influxwriter,dataprep


parser = argparse.ArgumentParser(description='Read weather from openweathermap')
parser.add_argument('--no-db',action='store_false',dest='useDB',default=True,
                    help="don't write output into the db; e.g. for testing")
parser.add_argument('--display',action='store_true',dest='printResults',default=False,
                    help="Print output to the screen")
parser.add_argument('--configFile',dest='config_file',default='./openweathermap.conf',
                    help="configuration file")

parser.add_argument('--current',action='store_true',dest='current',default=False,
                    help="Get the current weather")
parser.add_argument('--forecast',action='store_true',dest='forecast',default=False,
                    help="Get the forecast")

args = parser.parse_args()

def pretty_dict(d,indent=0):
    padding = " "*indent
    pref_len = 2+max(len(x) for x in d.keys())
    for x in d.items():
        print(f'{padding}{x[0]:{pref_len}}: {x[1]}')



if __name__ == '__main__':

    if not args.current and not args.forecast:
        print("One of --currrent or --forecast should be selected")
        sys.exit(1)

    cf = config.read_config(args.config_file)
    if args.current:
        j  = caller.current_weather_by_coor(lat = float(cf['DEFAULT']['lat']),
                                        lon = float(cf['DEFAULT']['lon']),
                                        apikey =    cf['DEFAULT']['key'],
                                        )
        d = dataprep.prepare_current_weather(j)
        if args.printResults:
            pretty_dict(d)

        if args.useDB:
            points = [dataprep.prepare_current_weather_influx(d)]
            #print(points)
            with influxwriter.get_client(host = cf['INFLUXDB']['host'],
                                         port = cf['INFLUXDB']['port']) \
                                          as client:
                influxwriter.initialise_db(client,cf['INFLUXDB']['database'])
                influxwriter.insert_data(client,points)
            pass

    if args.forecast:
        j  = caller.forecast_weather_by_coor(lat   = float(cf['DEFAULT']['lat']),
                                            lon    = float(cf['DEFAULT']['lon']),
                                            apikey =    cf['DEFAULT']['key'],
                                            )
        #del(j['list'])
        d = dataprep.prepare_forecast_weather(j)
        if args.printResults:
            for l in d:
                pretty_dict(l,indent=4)
                print()
        #print(j)
        if args.useDB:
            points = dataprep.prepare_forecast_weather_influx(d)
            #print(points)
            with influxwriter.get_client(host = cf['INFLUXDB']['host'],
                                         port = cf['INFLUXDB']['port']) \
                                      as client:
                influxwriter.initialise_db(client,cf['INFLUXDB']['database'])
                influxwriter.insert_data(client,points)
            pass
