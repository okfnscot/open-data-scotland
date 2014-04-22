import csv
import datetime
from string import Template


CSV_IN = "../scotland-data-portals.csv"
HTML_OUT = "/Users/ewan/git/open-data-scotland-pages/index.html"

today = datetime.datetime.today()
today = today.strftime("%d %B %Y")

HEAD = """
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
  <head>
    <link href="style.css" rel="stylesheet" type="text/css">
  </head>
  <body>
  <div id="container">
     <div id="header">
     <h1>Scotland Open Data Portals</h1>
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
  Last updated: %s. Source data at <a href="https://github.com/okfnscot/open-data-scotland">https://github.com/okfnscot/open-data-scotland</a>
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
    body = create_body(CSV_IN) 
    html = HEAD + body + FOOT
    with open(HTML_OUT, "w") as outfile:
        outfile.write(html)
        print("Writing to %s" % HTML_OUT)   
    
    
    
if __name__ == "__main__":
    main() 