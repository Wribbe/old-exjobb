all: mdoc.pdf

%.pdf : %.tex
	pdflatex $<
