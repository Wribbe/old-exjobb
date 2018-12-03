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

all: $(BIBS) commented

full both: $(BIBS) commented no_comments

commented: $(PDFS_COMMENTS)

no_comments: $(PDFS_NO_COMMENTS)


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


$(DIR_OUT)/%-no-comments.pdf : %.tex $(PLOTS) | $(DIR_OUT)
	$(call PP,pdflatex -output-directory $(DIR_OUT), $(filter %.tex,$^),$@,$(filter %.tex,$^))


%.pdf : $(DIR_PLOTS_SRC)/%.py plots.py | $(DIR_PLOTS)
	./plots.py $(filter-out plots.py,$^) $@


$(DIR_OUT)/%.bib : %_raw.bib | $(DIR_OUT)
	ln -sr $^ $@


tex/tidsschema.tex : py/tids.py | $(DIR_TEX)
	python $^ > $@


$(DIRS):
	@mkdir -p $@
