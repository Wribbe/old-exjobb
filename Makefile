
PDFS := $(patsubst %.tex,%.pdf,$(wildcard *.tex))
BBLS := $(patsubst %._raw.bbl,%.bbl,$(wildcard *raw.bib))

INPUTS := tex/tidsschema.tex

DIR_TEX := tex

all: $(INPUTS) $(PDFS) $(BBLS)

%.pdf : %.tex %.bbl $(INPUTS)
	pdflatex $(filter %.tex,$^)
	pdflatex $(filter %.tex,$^)

%.pdf : %.tex $(INPUTS)
	pdflatex $(filter %.tex,$^)

%.bbl : %.bib
	pdflatex $(patsubst %.bbl,%.tex,$@)
#	bibtex $(patsubst %.bbl,%,$@)
	biber $(patsubst %.bbl,%,$@)
	pdflatex $(patsubst %.bbl,%.tex,$@)

%.bib : %_raw.bib
	./clean_bib_urls.py $^ > $@

tex/tidsschema.tex : py/tids.py | $(DIR_TEX)
	@python $^ > $@

$(DIR_TEX):
	@mkdir $@
