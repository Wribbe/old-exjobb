DIR_ROOT := exjobb
DIR_OUT := $(DIR_ROOT)/out
DIR_TEX := $(DIR_ROOT)/tex

PDF:=$(DIR_OUT)/main.pdf

all: $(PDF)

$(DIR_OUT)/%:
	mkdir -p $@

define build_rule
$(DIR_OUT)/$1.pdf: $(DIR_TEX)/$1/$1.tex $(wildcard $(DIR_TEX)/$1/*.tex) | $(DIR_OUT)/$1
	TEXINPUTS=./$(DIR_TEX)/$1:$$$$TEXINPUTS pdflatex --output-directory $(DIR_OUT)/$1 $1.tex
endef

$(foreach dir,$(shell ls $(DIR_TEX)),$(eval $(call build_rule,$(dir))))
