#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Open Knowledge Scotland
# ----------------------------------------------------------------------------- 
# Author: Ewan Klein <ewan@raw-text.io>
# -----------------------------------------------------------------------------
# For license information, see LICENSE.txt
# -----------------------------------------------------------------------------
# 
# Script to convert  "Scotland's open data catalogues" CSV file into HTML
#

import argparse
import csv
import datetime
from string import Template


CSV_IN = "../scotland-data-portals.csv"
HTML_OUT = "../../open-data-scotland-pages/index.html"

today = datetime.datetime.today()
today = today.strftime("%d %B %Y")

HEAD = """
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
  <head>
    <title>Scotland's Open Data Portals</title>
    <link href="style.css" rel="stylesheet" type="text/css">
    <span id="forkongithub"><a href="https://github.com/okfnscot/open-data-scotland">Fork me on GitHub</a></span>
  </head>
  <body>

  <div id="container">
     <div id="header">
     <h1>Scotland's Open Data Catalogues</h1>
     </div>
     <div id="intro">
     <p>
     This page provides a  list of websites in Scotland
     that are partially or wholly focussed on making open data
     available. The list only includes sites that provide access to a <b>collection</b> of
     datasets, rather than just a single dataset.

    A further criterion for inclusion is that access to data is made available in at least
    one of the following modes:
    
    <ul>
     <li>bulk download in a machine readable format (e.g., CSV, RSS, XML);</li>
     <li>via a documented API; or</li>
     <li>as a SPARQL endpoint.</li>
    </ul>
     </p>
     
     <p>
     This list is preliminary and additions are very welcome. Send suggestions by email to okfnscot [AT] gmail.com, or fork the CSV data file and send a pull request.
     </div>
"""
BODY = """
  <div id="entry">
    <div id="title">
        <p>
        <a href="$url">$name</a>
        </p>        
        $datasets
    </div>
     <div id="description">
     <p>
      $description
     </p>
    </div>
 </div>
"""

FOOT = """
  </div>
  <div id="footer">
  Page generated automatically on %s. Source data at <a href="https://github.com/okfnscot/open-data-scotland">https://github.com/okfnscot/open-data-scotland</a>
  </div>
  </body>
<html>
""" % today

def datalist(datastr):
    if datastr == '':
        return datastr
    else:
        items = datastr.split(',') 
        list_items = '<ul id="dataset">\n'
        for i in items:
            i = i.strip()
            list_items = list_items + ("<li>\n        %s\n        </li>\n" % i)
        list_items = list_items +  '\n</ul>\n'
        
        return list_items

def create_body(fn):
    
    with open(fn) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        
        tmpl = Template(BODY)
        content = []
        
        for row in reader:
            try:
                (name, URL, level, sector, resources, description) = row
                description = description.replace('"','')
                description.strip()
                datasets = datalist(resources)
                content.append(tmpl.substitute(url=URL,
                                               name=name, 
                                               datasets=datasets,
                                               description=description))
            except ValueError:
                pass
    body = ''.join(content)
    return body



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('outfile')
    
    args = parser.parse_args()
      
    body = create_body(args.infile) 
    html = HEAD + body + FOOT
    with open(args.outfile, "w") as outfile:
        outfile.write(html)
        print("Writing to %s" % args.outfile)   
    
    
    
if __name__ == "__main__":
    main() 
