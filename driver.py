import consume

def PrintHeader(consumeObj, id, catList):
    out = "fuelbed"
    consumeObj.fuelbed_fccs_ids = id
    results = consumeObj.results()['consumption']
    for i in catList:
        out += "," + i.upper()
        for j in results[i].keys():
            out += "," + j
    print(out)

def PrintCsv(consumeObj, idList):
	### - top-level catagory list
    catagoryList = ['summary', 'canopy', 'ground fuels', 'litter-lichen-moss', 'nonwoody', 'shrub', 'woody fuels']
    
    PrintHeader(consumeObj, idList, catagoryList)

    ### - loop through all the fuelbeds
    for id in idList:
        out = id
        consumeObj.fuelbed_fccs_ids = id
        results = consumeObj.results()['consumption']
        for i in catagoryList:
        	### - this is a divider column for each top-level catagory
            out += "," + "-{}-".format(i)
            for j in results[i].keys():
                out += "," + str(results[i][j]['total'][0])
        print(out)

def SimpleSummary(consumeObj, idList):
	for i in idList:
	    consumeObj.fuelbed_fccs_ids = i
	    print "Fuelbed {0}:".format(i)
	    print "\ttotal = {0}".format(consumeObj.results()['consumption']['summary']['total']['total'])
	    print "\tcanopy = {0}".format(consumeObj.results()['consumption']['summary']['canopy']['total'])
	    print "\tground fuels= {0}".format(consumeObj.results()['consumption']['summary']['ground fuels']['total'])
	    print "\tlitter-lichen-moss= {0}".format(consumeObj.results()['consumption']['summary']['litter-lichen-moss']['total'])
	    print "\tnonwoody= {0}".format(consumeObj.results()['consumption']['summary']['nonwoody']['total'])
	    print "\tshrub= {0}".format(consumeObj.results()['consumption']['summary']['shrub']['total'])
	    print "\twoody fuels= {0}".format(consumeObj.results()['consumption']['summary']['woody fuels']['total'])


#-------------------------------------------------------------------------------
# Start
#-------------------------------------------------------------------------------

### - this is the "database" of information from FCCS
consumer = consume.FuelConsumption(fccs_file = "fccs_pyconsume_input.xml")

### - this gets a list of the fuelbed numbers that are in the above file.
ids = [str(i[0]) for i in consumer.FCCS.data]

### - this file contains configuration data (windspeed, percent blackened, etc.)
consumer.load_scenario("input_1.csv")

### - summarizes results across all the fuelbeds
PrintCsv(consumer, ids)
