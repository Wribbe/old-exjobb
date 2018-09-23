
PDFS := $(patsubst %.tex,%.pdf,$(wildcard *.tex))
INPUTS := tex/tidsschema.tex

DIR_TEX := tex

all: $(INPUTS) $(PDFS)

%.pdf : %.tex $(INPUTS)
	pdflatex $(filter %.tex,$^)

%.pdf : %.tex %.bib $(INPUTS)
	pdflatex $(filter %.tex,$^)
	bibtex $(patsubst %.bib,%,$(filter %.bib,$^))
	pdflatex $(filter %.tex,$^)
	pdflatex $(filter %.tex,$^)

tex/tidsschema.tex : py/tids.py | $(DIR_TEX)
	@python $^ > $@

$(DIR_TEX):
	@mkdir $@
