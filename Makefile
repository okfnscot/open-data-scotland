HTMLDIR := ../open-data-scotland-pages
HTML-OUT := index.html

CSV-IN := scotland-data-portals.csv
BUILDER := scripts/csv2html.py

ci: html
	cd $(HTMLDIR); git ci -m "Updated HTML" $(HTML-OUT); git push

html: $(CSV)
	python $(BUILDER) $(CSV-IN) $(HTMLDIR)/$(HTML-OUT)

