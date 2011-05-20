import consume
import sys

def PrintHeader(results, catList):
    out = "fuelbed"
    for i in catList:
        out += "," + i.upper()
        ### - this needs to stay in sync with the way the data is printed
        sortedKeys = sorted(results[i].keys())
        for j in sortedKeys:
            out += "," + j
    print(out)

def PrintCsv(consumeObj, idList):
	### - top-level catagory list
    catagoryList = ['summary', 'canopy', 'ground fuels', 'litter-lichen-moss',
        'nonwoody', 'shrub', 'woody fuels']

    consumeObj.fuelbed_fccs_ids = idList
    results = consumeObj.results()['consumption']
    PrintHeader(results, catagoryList)
    for fbIdx in xrange(0, len(idList)):
        out = idList[fbIdx]
        for cat in catagoryList:
        	### - this is a divider column for each top-level catagory
            out += "," + "-{}-".format(cat)
            ### - this needs to stay in sync with the way the header is printed
            sortedKeys = sorted(results[cat].keys())
            for key in sortedKeys:
                out += "," + str(results[cat][key]['total'][fbIdx])
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
consumer = consume.FuelConsumption(fccs_file = "input_data/fccs_pyconsume_input.xml")

### - this gets a list of the fuelbed numbers that are in the above file.
ids = [str(i[0]) for i in consumer.FCCS.data]

### - this file contains configuration data (windspeed, percent blackened, etc.)
if len(sys.argv) > 1:
        consumer.load_scenario(sys.argv[1])
        PrintCsv(consumer, ['1', '2', '1001'])
else:
    ecoregions = ['western', 'boreal', 'southern']
    for region in ecoregions:
        consumer.load_scenario("{}.csv".format(region))
        ### - summarizes results across all the fuelbeds
        PrintCsv(consumer, ids)
