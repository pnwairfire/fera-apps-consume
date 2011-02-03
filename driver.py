import consume

#-------------------------------------------------------------------------------
# Start
#-------------------------------------------------------------------------------
consumer = consume.FuelConsumption(fccs_file = "reference216_input.xml")
ids = [str(i[0]) for i in consumer.FCCS.data]
consumer.load_scenario("input_0.csv")
for i in ids:
    consumer.fuelbed_fccs_ids = i
    #consumer.report(csv="reference216_output.csv")
    #consumer.report(stratum='total')
    print "Fuelbed {0}\t= {1}".format(i, consumer.results()['consumption']['summary']['total']['total'])
