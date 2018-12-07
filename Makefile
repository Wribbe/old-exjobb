#!/usr/bin/env make -f

DIR_TEX := tex
DIR_OUT := out
DIR_PLOTS := figures/plots
DIR_PLOTS_SRC := src/plots

PERCENT := %
$(eval DIRS := $(foreach var,$(filter-out %_$(PERCENT)%,$(filter DIR_%,$(shell cat Makefile))),$$($(var))))

SUF_NOCO := _no_comments
SUF_CO := _comments

BASE_NAMES := $(patsubst %.tex,%,$(wildcard *.tex))
BASE_NAMES := $(filter report,$(BASE_NAMES))
PDFS := $(foreach n,$(BASE_NAMES),$n$(SUF_NOCO).pdf $n$(SUF_CO).pdf)
PDFS := $(foreach p,$(PDFS),$(DIR_OUT)/$p)

PLOTS := $(patsubst %.py,$(DIR_PLOTS)/%.pdf,$(notdir $(wildcard $(DIR_PLOTS_SRC)/*.py)))
BIBS := $(PDFS:.pdf=.bib)
TEXS := $(PDFS:.pdf=.tex)
SRC_LINKS := $(PDFS:.pdf=)

IMGS := $(wildcard images/*)

all: $(SRC_LINKS) $(TEXS) $(BIBS) commented

full both: all no_comments

commented: $(filter-out %$(SUF_NOCO).pdf,$(PDFS))

no_comments: $(filter %$(SUF_NOCO).pdf,$(PDFS))

re:
	$(MAKE) -B $(filter-out $@,$(MAKECMDGOALS))


PP = \
	pdf_out=$$($1 $2 | tee /dev/tty); \
	rerun_biber=$$(echo "$$pdf_out" | grep -E "undefined references|entry could not be found"); \
	rerun_links=$$(echo "$$pdf_out" | grep -E "Rerun to get cross-references right"); \
	if [ -n "$$rerun_biber" ]; then \
	  biber $(2:.tex=); \
		$1 $2;\
	elif [ -n "$$rerun_links" ]; then \
		$1 $2; \
	fi


%.pdf : %.tex % %.bib $(PLOTS) $(IMGS) | $(DIR_OUT)
	$(call PP,pdflatex -output-directory $(DIR_OUT), $(filter %.tex,$^))


%.pdf : $(DIR_PLOTS_SRC)/%.py plots.py | $(DIR_PLOTS)
	./plots.py $(filter-out plots.py,$^) $@


$(DIR_OUT)/%$(SUF_NOCO).tex : %.tex | $(DIR_OUT)
	./tex_format.py $^ bibfile=$(notdir $(@:.tex=)) > $@


$(DIR_OUT)/%$(SUF_CO).tex : %.tex | $(DIR_OUT)
	./tex_format.py $^ COMMENTS bibfile=$(notdir $(@:.tex=)) > $@


$(DIR_OUT)/%$(SUF_NOCO).bib : %_raw.bib | $(DIR_OUT)
	python raw2bib.py $^ > $@


$(DIR_OUT)/%$(SUF_CO).bib : %_raw.bib | $(DIR_OUT)
	python raw2bib.py $^ > $@


tex/tidsschema.tex : py/tids.py | $(DIR_TEX)
	python $^ > $@


$(DIRS):
	@mkdir -p $@

$(DIR_OUT)/%$(SUF_NOCO): | $(DIR_OUT)
	[ -d "tex/$*" ] || mkdir -p tex/$*
	ln -sr tex/$* $@

$(DIR_OUT)/%$(SUF_CO): | $(DIR_OUT)
	[ -d "tex/$*" ] || mkdir -p tex/$*
	ln -sr tex/$* $@

clean:
	rm -rf out

.PHONY : clean all full both commented no_comments
