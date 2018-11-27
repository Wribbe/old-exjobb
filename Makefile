
DIR_TEX := tex
DIR_OUT := out
DIR_PLOTS := figures/plots
DIR_PLOTS_SRC := src/plots

PDFS := $(patsubst %.tex,$(DIR_OUT)/%.pdf,$(wildcard *.tex))
BBLS := $(patsubst %_raw.bib,$(DIR_OUT)/%.bib,$(wildcard *raw.bib))
BIBS := $(patsubst %.bbl,%.bib,$(BBLS))
IMGS := $(wildcard images/*)

PP := pdflatex -output-directory $(DIR_OUT)

INPUTS := tex/tidsschema.tex

PLOTS := $(patsubst %.py,$(DIR_PLOTS)/%.pdf,$(notdir $(wildcard $(DIR_PLOTS_SRC)/*.py)))

all: $(DIR_OUT) $(INPUTS) $(BIBS) $(PLOTS) $(PDFS)
#all: $(DIR_OUT) $(INPUTS) $(BBLS) $(BIBS) $(PLOTS) $(PDFS)

$(DIR_OUT)/%.pdf : %.tex %_raw.bib $(INPUTS) $(IMGS) $(PLOTS)
	$(PP) $(filter %.tex,$^)
	cd $(DIR_OUT) && biber $(notdir $(patsubst %.pdf,%,$@))
	$(PP) $(filter %.tex,$^)
	$(PP) $(filter %.tex,$^)

$(DIR_OUT)/mdoc.pdf : mdoc.tex $(INPUTS) | $(DIR_OUT)
	$(PP) $(filter %.tex,$^)

#$(DIR_OUT)/%.bbl : $(DIR_OUT)/%.bib
#	$(PP) $(notdir $(patsubst %.bbl,%.tex,$@))
#	bibtex $(patsubst %.bbl,%,$@)
#	$(PP) $(notdir $(patsubst %.bbl,%.tex,$@))

$(DIR_OUT)/%.bib : %_raw.bib
	./clean_bib_urls.py $^ > $@

$(DIR_PLOTS)/%.pdf : $(DIR_PLOTS_SRC)/%.py plots.py
	./plots.py $(filter-out plots.py,$^) $@

tex/tidsschema.tex : py/tids.py | $(DIR_TEX)
	python $^ > $@

$(DIR_TEX):
	mkdir $@

$(DIR_OUT):
	mkdir $@

$(DIR_PLOTS):
	mkdir $@
