HTMLDIR := ../open-data-scotland-pages
HTML-OUT := index.html

CSV-IN := scotland-data-catalogues.csv
BUILDER := scripts/csv2html.py

ci: html data
	cd $(HTMLDIR); git ci -m "Updated HTML" $(HTML-OUT); git push

html: data
	python $(BUILDER) $(CSV-IN) $(HTMLDIR)/$(HTML-OUT)

data: $(CSV-IN)
	git ci -m "Updated CSV file" $<; git push



