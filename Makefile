all: mdoc.pdf

%.pdf : %.tex %.bib
	pdflatex $(filter %.tex,$^)
	bibtex $(patsubst %.bib,%,$(filter %.bib,$^))
	pdflatex $(filter %.tex,$^)
	pdflatex $(filter %.tex,$^)
