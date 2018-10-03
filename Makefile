
PDFS := $(patsubst %.tex,%.pdf,$(wildcard *.tex))
INPUTS := tex/tidsschema.tex

DIR_TEX := tex

all: $(INPUTS) $(PDFS)

%.pdf : %.tex %.bbl $(INPUTS)
	pdflatex $(filter %.tex,$^)
	pdflatex $(filter %.tex,$^)

%.pdf : %.tex $(INPUTS)
	pdflatex $(filter %.tex,$^)

%.bbl : %.bib
	pdflatex $(patsubst %.bbl,%.tex,$@)
	bibtex $(patsubst %.bbl,%,$@)
	pdflatex $(patsubst %.bbl,%.tex,$@)

tex/tidsschema.tex : py/tids.py | $(DIR_TEX)
	@python $^ > $@

$(DIR_TEX):
	@mkdir $@
