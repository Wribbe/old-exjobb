DIR_OUT:= exjobb/out

PDF:=$(DIR_OUT)/main.pdf

all: $(PDF)

$(DIR_OUT)/%.pdf : exjobb/tex/%/%.tex $(wilcard exjobb/tex/%/*.tex) | $(DIR_OUT)
	pdflatex --output-directory $(DIR_OUT) $^

$(DIR_OUT):
	mkdir -p $@
