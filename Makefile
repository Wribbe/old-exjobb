
DIR_TEX := tex
DIR_OUT := out

PDFS := $(patsubst %.tex,$(DIR_OUT)/%.pdf,$(wildcard *.tex))
BBLS := $(patsubst %_raw.bib,$(DIR_OUT)/%.bib,$(wildcard *raw.bib))
BIBS := $(patsubst %.bib,%.bbl,$(BBLS))
IMGS := $(wildcard images/*)

PP := pdflatex -output-directory $(DIR_OUT)

INPUTS := tex/tidsschema.tex

all: $(DIR_OUT) $(INPUTS) $(BBLS) $(BIBS) $(PDFS)

$(DIR_OUT)/%.pdf : %.tex %.bbl %_raw.bib $(INPUTS) $(IMGS)
	$(PP) $(filter %.tex,$^)
	$(PP) $(filter %.tex,$^)

$(DIR_OUT)/%.pdf : %.tex $(INPUTS) | $(DIR_OUT)
	$(PP) $(filter %.tex,$^)

$(DIR_OUT)/%.bbl : $(DIR_OUT)/%.bib
	$(PP) $(notdir $(patsubst %.bbl,%.tex,$@))
#	bibtex $(patsubst %.bbl,%,$@)
	cd $(DIR_OUT) && biber $(notdir $(patsubst %.bbl,%,$@))
	$(PP) $(notdir $(patsubst %.bbl,%.tex,$@))

$(DIR_OUT)/%.bib : %_raw.bib
	./clean_bib_urls.py $^ > $@

tex/tidsschema.tex : py/tids.py | $(DIR_TEX)
	python $^ > $@

$(DIR_TEX):
	mkdir $@

$(DIR_OUT):
	mkdir $@
