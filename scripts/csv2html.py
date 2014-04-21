import csv
from string import Template

CSV_IN = "../scotland-data-portals.csv"
HTML_OUT = "/Users/ewan/git/open-data-scotland-pages/index.html"

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
  </body>
<html>
"""

def create_body(fn):
    with open(fn) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        
        tmpl = Template(BODY)
        content = []
        
        for row in reader:
            try:
                (name, URL, level, sector, access, description) = row
                description = description.replace('"','')
                description.strip()
                content.append(tmpl.substitute(url=URL,
                                               name=name, 
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