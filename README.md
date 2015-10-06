# Consume

### Purpose/Description:
Consume calculates consumption and emission results based on a number of input parameters. The core Consume code was designed for interactive use in a REPL (read, evaluate, print, loop) environment. FERA has wrapped the core code to provide an application interface. Run the wrapper (consume_batch.py) with no arguments to see usage instructions.

```

$ python consume_batch.py 
usage: consume_batch.py [-h] [-f loadings file] [-x output columns]
                        [-l message level] [--metric] [-o output filename]
                        [burn type	(activity | natural)]
                        [input file	csv format]

    Consume predicts fuel consumption, pollutant emissions, and heat release
    based on input fuel loadings and environmental variables.  This command
    line interface requires a specified burn type (either activity or natural),
    environmental variables input file (csv format), and fuel loadings file
    (generated by FCCS 3.0, csv format), and.  A sample fuel loadings file
    (fuel_loadings.csv) and environmental inputs file (input.csv) have been
    provided. For more information on FCCS input files and results,
    please see: LINK.

positional arguments:
  burn type	(activity | natural)
  input file	(csv format)

optional arguments:
  -h, --help            show this help message and exit
  -f loadings file      Specify the fuel loadings file for consume to use. Run
                        the FCCS batch processor over the fuelbeds for which
                        you want to generate consumption/emission results to
                        create a fuel loadings file.
  -x output columns     Specify the output column configuration file for
                        consume to use
  -l message level      Specify the detail level of messages (1 | 2 | 3). 1 =
                        fewest messages 3 = most messages
  --metric              Indicate that columns should be converted to metric
                        units.
  -o output filename    Specify the name of the Consume output results file.

Examples:
    // display help (this text)
    python consume_batch.py

    // Simple case, natural fuel types, required input file (uses built-in loadings file)
    python consume_batch.py natural input_natural.csv

    // Specify an alternative loadings file
    consume_batch.exe natural input_natural.csv -f my_loadings.xml

    // Specify a column configuration file. Please see the documentation for details.
    consume_batch.exe activity input_activity.csv -x output_summary.csv

```

### Building
Consume is written in Python so there is no build. Consume runs under both Python 2 an 3

### Tests
Consume has regression tests. Run them like so (note that Consume runs under both Python 2 and 3):

```
$ ./run_regression_tests.sh 
Python 2.7.10 :: Continuum Analytics, Inc.

0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/western_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/southern_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/boreal_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/activity_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/2_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/3_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/4_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/5_out.csv
0 = failed, 7992 compared:	activity_emissions_kgha.csv
0 = failed, 8029 compared:	western_emissions.csv
0 = failed, 8029 compared:	activity_emissions.csv
0 = failed, 7992 compared:	activity_emissions_kgha_alpha.csv
0 = failed, 7918 compared:	activity_emissions_kgha_random.csv


$ ./rr.sh 
Python 3.4.3 :: Continuum Analytics, Inc.

0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/western_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/southern_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/boreal_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/activity_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/2_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/3_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/4_out.csv
0 = failed, 15300 compared:	/home/kjells/fera/Consume4/test/results/5_out.csv
0 = failed, 7992 compared:	activity_emissions_kgha.csv
0 = failed, 8029 compared:	western_emissions.csv
0 = failed, 8029 compared:	activity_emissions.csv
0 = failed, 7992 compared:	activity_emissions_kgha_alpha.csv
0 = failed, 7918 compared:	activity_emissions_kgha_random.csv

```

### Problems/Quirks

### Links
name (link)