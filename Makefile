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
BBLS := $(patsubst %_raw.bib,$(DIR_OUT)/%.bbl,$(wildcard *.bib))
BIBS := $(patsubst %.bbl,%.bib,$(BBLS))
IMGS := $(wildcard images/*)

PP := pdflatex -output-directory $(DIR_OUT)

INPUTS := tex/tidsschema.tex

PLOTS := $(patsubst %.py,$(DIR_PLOTS)/%.pdf,$(notdir $(wildcard $(DIR_PLOTS_SRC)/*.py)))


all:   commented

full both: commented non-commented

deps_both: $(BIBS) $(BBLS) $(PLOTS) $(INPUTS)

commented: deps_both $(PDFS_COMMENTED)

non-commented: deps_both $(PDFS_NON_COMMENTED)

#	$(PP) -draftmode "\def\visibleComments{1} $(foreach f,$(filter %.tex,$^),\input{$(f)})"
#	cd $(DIR_OUT) && biber $(notdir $(patsubst %-commented.pdf,%,$@))
#	$(PP) -draftmode "\def\visibleComments{1} $(foreach f,$(filter %.tex,$^),\input{$(f)})"

$(DIR_OUT)/%-commented.pdf : %.tex $(INPUTS) $(IMGS) $(PLOTS)
	$(PP) "\def\visibleComments{1} $(foreach f,$(filter %.tex,$^),\input{$(f)})"
	@mv $(patsubst %-commented.pdf,%.pdf,$@) $@

$(DIR_OUT)/%-non-commented.pdf : %.tex $(INPUTS) $(IMGS) $(PLOTS)
	$(PP) $(filter %.tex,$^)
	@mv $(patsubst %-non-commented.pdf,%.pdf,$@) $@


#$(DIR_OUT)/mdoc.pdf : mdoc.tex $(INPUTS) | $(DIR_OUT)
#	$(PP) $(filter %.tex,$^)

#$(DIR_OUT)/%.bbl : $(DIR_OUT)/%.bib
#	$(PP) $(notdir $(patsubst %.bbl,%.tex,$@))
#	bibtex $(patsubst %.bbl,%,$@)
#	$(PP) $(notdir $(patsubst %.bbl,%.tex,$@))

DEP_BIB_BBL :=  %_raw.bib | $(DIR_OUT)


$(DIR_OUT)/%.bbl : $(DEP_BIB_BBL)
	$(PP) -draft-mode $(notdir $(@:.bbl=.tex))
	cd $(DIR_OUT) && biber $(notdir $(@:.bbl=))
	$(PP) -draft-mode $(notdir $(@:.bbl=.tex))

$(DIR_OUT)/%.bib : $(DEP_BIB_BBL)
	./clean_bib_urls.py $^ > $@

$(DIR_PLOTS)/%.pdf : $(DIR_PLOTS_SRC)/%.py plots.py | $(DIR_PLOTS)
	./plots.py $(filter-out plots.py,$^) $@

tex/tidsschema.tex : py/tids.py | $(DIR_TEX)
	python $^ > $@

$(DIRS):
	@mkdir -p $@

.PHONY: all commented non-commented deps_both full both
