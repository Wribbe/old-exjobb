#!/usr/bin/env make -f

DIR_TEX := tex
DIR_OUT := out
DIR_PLOTS := figures/plots
DIR_PLOTS_SRC := src/plots

PERCENT := %
$(eval DIRS := $(foreach var,$(filter-out %_$(PERCENT)%,$(filter DIR_%,$(shell cat Makefile))),$$($(var))))

PDFS := $(patsubst %.tex,$(DIR_OUT)/%.pdf,$(wildcard *.tex))
PDFS_COMMENTED = $(patsubst %.pdf,%-commented.pdf,$(PDFS))
PDFS_NON_COMMENTED = $(patsubst %.pdf,%-non-commented.pdf,$(PDFS))
BBLS := $(patsubst %_raw.bib,$(DIR_OUT)/%.bib,$(wildcard *raw.bib))
BIBS := $(patsubst %.bbl,%.bib,$(BBLS))
IMGS := $(wildcard images/*)

PP := pdflatex -output-directory $(DIR_OUT)

INPUTS := tex/tidsschema.tex

PLOTS := $(patsubst %.py,$(DIR_PLOTS)/%.pdf,$(notdir $(wildcard $(DIR_PLOTS_SRC)/*.py)))

all: commented non-commented
#all: $(DIR_OUT) $(INPUTS) $(BBLS) $(BIBS) $(PLOTS) $(PDFS)

commented: $(BIBS) $(PDFS_COMMENTED)

non-commented: $(BIBS) $(PDFS_NON_COMMENTED)

$(DIR_OUT)/%-commented.pdf : %.tex %_raw.bib $(INPUTS) $(IMGS) $(PLOTS)
	$(PP) "\def\visibleComments{1} $(foreach f,$(filter %.tex,$^),\input{$(f)})"
	cd $(DIR_OUT) && biber $(notdir $(patsubst %-commented.pdf,%,$@))
	$(PP) "\def\visibleComments{1} $(foreach f,$(filter %.tex,$^),\input{$(f)})"
	$(PP) "\def\visibleComments{1} $(foreach f,$(filter %.tex,$^),\input{$(f)})"
	@mv $(patsubst %-commented.pdf,%.pdf,$@) $@

$(DIR_OUT)/%-non-commented.pdf : %.tex %_raw.bib $(INPUTS) $(IMGS) $(PLOTS)
	$(PP) $(filter %.tex,$^)
	cd $(DIR_OUT) && biber $(notdir $(patsubst %-non-commented.pdf,%,$@))
	$(PP) $(filter %.tex,$^)
	$(PP) $(filter %.tex,$^)
	@mv $(patsubst %-non-commented.pdf,%.pdf,$@) $@

#$(DIR_OUT)/mdoc.pdf : mdoc.tex $(INPUTS) | $(DIR_OUT)
#	$(PP) $(filter %.tex,$^)

#$(DIR_OUT)/%.bbl : $(DIR_OUT)/%.bib
#	$(PP) $(notdir $(patsubst %.bbl,%.tex,$@))
#	bibtex $(patsubst %.bbl,%,$@)
#	$(PP) $(notdir $(patsubst %.bbl,%.tex,$@))

$(DIR_OUT)/%.bib : %_raw.bib
	./clean_bib_urls.py $^ > $@

$(DIR_PLOTS)/%.pdf : $(DIR_PLOTS_SRC)/%.py plots.py | $(DIRS)
	./plots.py $(filter-out plots.py,$^) $@

tex/tidsschema.tex : py/tids.py | $(DIR_TEX)
	python $^ > $@

$(DIRS):
	@mkdir $@

.PHONY: all commented non-commented
