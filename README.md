ddtv
====

A set of scripts for visualizing data for/from the dvm-dos-tem ecosystem model.

Each script has some decent help with the --help flag.


Requirements
------------

I am not certain that all of these are necessary, but this is the envrionment 
I have:

    $ pip freeze
    GDAL==1.9.1
    PyMySQL==0.5
    basemap==1.0.6
    distribute==0.6.34
    git-remote-helpers==0.1.0
    ipython==0.13.1
    matplotlib==1.2.0
    netCDF4==1.0.2
    numpy==1.6.2
    pandas==0.10.1
    python-dateutil==2.1
    pytz==2012j
    scipy==0.11.0
    six==1.2.0
    virtualenv==1.8.4
    wsgiref==0.1.2
    yolk==0.4.3

Examples
------------

    $ ./heatmap_year_vs_month.py -s "examples/hm-polar1.png" -m polar -c 1 -pft 1 -v VEGC output-archives/after-phen/output-sp.nc
![Alt text](examples/hm-polar1.png "Example polar plot")

