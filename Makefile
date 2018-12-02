#!/usr/bin/env make -f

DIR_TEX := tex
DIR_OUT := out
DIR_PLOTS := figures/plots
DIR_PLOTS_SRC := src/plots

PERCENT := %
$(eval DIRS := $(foreach var,$(filter-out %_$(PERCENT)%,$(filter DIR_%,$(shell cat Makefile))),$$($(var))))

TEXS := $(filter report.tex,$(wildcard *.tex))
PDFS_COMMENTS := $(patsubst %.tex,$(DIR_OUT)/%-comments.pdf,$(TEXS))
PDFS_NO_COMMENTS := $(patsubst %.tex,$(DIR_OUT)/%-no-comments.pdf,$(TEXS))

PLOTS := $(patsubst %.py,$(DIR_PLOTS)/%.pdf,$(notdir $(wildcard $(DIR_PLOTS_SRC)/*.py)))
BIBS := $(patsubst %_raw.bib,$(DIR_OUT)/%.bib,$(wildcard *_raw.bib))

all: $(BIBS) $(PDFS_COMMENTS)

PP = \
	pdf_out=$$($1 $2 | tee /dev/tty); \
	if [ -n $$(grep "LaTeX Warning: There were undefined references." "$$pdf_out") ]; then \
		(cd "$(DIR_OUT)" && biber $(4:.tex=)); \
		$1 $2;\
	fi; \
	mv $(DIR_OUT)/$(4:.tex=.pdf) $3;


$(DIR_OUT)/%-comments.pdf : %.tex $(PLOTS) | $(DIR_OUT)
	$(call PP,pdflatex -output-directory $(DIR_OUT), \
		"\def\visibleComments{1} $(foreach f,$(filter %.tex,$^),\input{$(f)})",\
	  $@,\
		$(filter %.tex,$^)\
	)



%.pdf : $(DIR_PLOTS_SRC)/%.py plots.py | $(DIR_PLOTS)
	./plots.py $(filter-out plots.py,$^) $@


$(DIR_OUT)/%.bib : %_raw.bib | $(DIR_OUT)
	ln -sr $^ $@

#PDFS_COMMENTED = $(patsubst %.pdf,%-commented.pdf,$(PDFS))
#PDFS_NON_COMMENTED = $(patsubst %.pdf,%-non-commented.pdf,$(PDFS))
#BBLS := $(patsubst %_raw.bib,$(DIR_OUT)/%.bbl,$(wildcard *.bib))
#BIBS := $(patsubst %.bbl,%.bib,$(BBLS))
#IMGS := $(wildcard images/*)
#
#LOGS := $(patsubst %.pdf,%.log,$(PDFS_COMMENTED) $(PDFS_NON_COMMENTED))
#LOG_CHECKS := $(LOGS:.log=.logcheck)
#
#BBL_SENTINELS := $(LOGS:.log=.bblsentinel)
#LOG_RELATED := $(LOGS) $(LOG_CHECKS) $(BBL_SENTINELS)
#
#PP = pdflatex -output-directory $(DIR_OUT) $(1) | tee $(2) 2>&1
#
#INPUTS := tex/tidsschema.tex
#
#PLOTS := $(patsubst %.py,$(DIR_PLOTS)/%.pdf,$(notdir $(wildcard $(DIR_PLOTS_SRC)/*.py)))
#
#.SECONDARY :
#
#all: commented
#
#full both: commented non-commented
#
#deps_both: $(LOG_RELATED) $(PLOTS) $(BIBS) $(BBLS) $(INPUTS)
#
#commented:  deps_both $(PDFS_COMMENTED)
#
#non-commented: deps_both $(PDFS_NON_COMMENTED)
#
#
#$(DIR_OUT)/%-commented.log : %.tex $(INPUTS) $(IMGS) $(PLOTS) | $(DIR_OUT)
#	$(call PP,"\def\visibleComments{1} $(foreach f,$(filter %.tex,$^),\input{$(f)})",$@)
#
#
#$(DIR_OUT)/%-non-commented.log : %.tex $(INPUTS) $(IMGS) $(PLOTS) | $(DIR_OUT)
#	$(call PP,$(filter %.tex,$^),$@)
#
#
#$(DIR_OUT)/%.logcheck: $(DIR_OUT)/%.log | $(DIR_OUT)
#	@[ -f $@ ] || touch $(@:.logcheck=.bblsentinel)
#	[ -z $(grep "LaTeX Warning: There were undefined references." "$^") ] || touch $(@:.logcheck=.bblsentinel)
#	touch $@
#
#
#%.bblsentinel :
#
#%-non-commented.pdf : %.logcheck %.bblsentinel
#	mv $(@:-non-commented.pdf=.pdf) $@
#
#
#%-commented.pdf : %.logcheck %.bblsentinel
#	mv $(@:-commented.pdf=.pdf) $@
#
#
#$(DIR_OUT)/%.bbl : $(DIR_OUT)/%.bblsentinel
#	[ -f $@ ] || $(call PP,-draft-mode $(notdir $(@:.bbl=.tex)),/dev/null)
#	cd $(DIR_OUT) && biber $(notdir $(@:.bbl=))
#	$(call PP,-draft-mode $(notdir $(@:.bbl=.tex)),/dev/null)
#
#
#$(DIR_OUT)/%.bib : %_raw.bib | $(DIR_OUT)
#	./clean_bib_urls.py $^ > $@
#
#
#$(DIR_PLOTS)/%.pdf : $(DIR_PLOTS_SRC)/%.py plots.py | $(DIR_PLOTS)
#	./plots.py $(filter-out plots.py,$^) $@
#
#
#tex/tidsschema.tex : py/tids.py | $(DIR_TEX)
#	python $^ > $@
#
#
$(DIRS):
	@mkdir -p $@
#
#
#.PHONY: all commented non-commented deps_both full both
