# Makefile for latex documents by Darren Atkinson (datkinson@scu.edu):
# - provides built-in rules for generating and viewing DVI, PDF, and PS files
# - automatically detects dependencies
# - handles conversion from FIG to EPS files
# - handles \input and \include commands
# - reruns latex if any ancillary data file changes
# - supports bibtex


# list of targets to make

TARGETS	= master.pdf


# programs used by later rules

PDFLATEX	= pdflatex
LATEX		= latex
BIBTEX		= bibtex -min-crossrefs=10
DVIPS		= dvips
EPS2PDF		= epstopdf
FIG2DEV		= fig2dev
VIEWDVI		= open
VIEWPDF		= open
VIEWPS		= open


# variables used by later rules

DEPEND	= \
-e 's/%.*//g' \
-e '/usepackage/s/,/.sty /g' \
-e '/bibliography/s/,/.bib /g' \
-e 's/^.*\\input{\([^}]*\)}/\1.tex/p' \
-e 's/^.*\\include{\([^}]*\)}/\1.tex/p' \
-e 's/^.*\\documentclass.*{\([^}]*\)}/\1.cls/p' \
-e 's/^.*\\usepackage.*{\([^}]*\)}/\1.sty/p' \
-e 's/^.*\\bibliography{\([^}]*\)}/\1.bib/p' \
-e 's/^.*\\bibliographystyle{\([^}]*\)}/\1.bst/p' \
-e 's/^.*\\lstinputlisting.*{\([^}]*\)}.*/\1/p' \
-e 's/^.*\\includegraphics.*{\([^}]*.jpg\)}.*/\1/p' \
-e 's/^.*\\includegraphics.*{\([^}]*.pdf\)}.*/\1/p' \
-e 's/^.*\\includegraphics.*{\([^}]*\)}.*/\1.pdf/p'

CATGEN	= \
grep -v relax $*.aux $*.bbl $*.loa $*.lof $*.lot $*.toc \
`sed -n 's/^..input{\(.*\)}/\1/p' $*.aux 2>/dev/null` 2>/dev/null


# suffix rules

.SUFFIXES:	.bbl .blg .dvi .eps .fig .pdf .ps .tex

.dvi.ps:
		@set -x; $(DVIPS) -o $@ $<

.fig.pdf:
		@set -x; $(FIG2DEV) -L pdf $< $@

.fig.eps:
		@set -x; $(FIG2DEV) -L eps $< $@

.eps.pdf:
		@set -x; $(EPS2PDF) $< > $@

.blg.bbl:
		@set -x; $(BIBTEX) $*

.tex.dvi:
		@$(CATGEN) > $*.tmp; set -x; $(LATEX) $*
		@$(CATGEN) | diff - $*.tmp | \
		egrep "citation|bibstyle|bibdata" >/dev/null && \
		(set -x; $(BIBTEX) $*) || true
		@until $(CATGEN) | diff - $*.tmp >/dev/null; do \
		$(CATGEN) > $*.tmp; (set -x; $(LATEX) $*) || break; done
		@rm -f $*.tmp

.tex.pdf:
		@$(CATGEN) > $*.tmp; set -x; $(PDFLATEX) $*
		@$(CATGEN) | diff - $*.tmp | \
		egrep "citation|bibstyle|bibdata" >/dev/null && \
		(set -x; $(BIBTEX) $*) || true
		@until $(CATGEN) | diff - $*.tmp >/dev/null; do \
		$(CATGEN) > $*.tmp; (set -x; $(PDFLATEX) $*) || break; done
		@rm -f $*.tmp


# fake targets

all:		$(TARGETS)

pdf:		$(TARGETS)

dvi:		$(TARGETS:.pdf=.dvi)

ps:		$(TARGETS:.pdf=.ps)

viewpdf:	$(TARGETS)
		@for FILE in $?; do (set -x; $(VIEWPDF) $$FILE) & done

viewdvi:	$(TARGETS:.pdf=.dvi)
		@for FILE in $?; do (set -x; $(VIEWDVI) $$FILE) & done

viewps:		$(TARGETS:.pdf=.ps)
		@for FILE in $?; do (set -x; $(VIEWPS) $$FILE) & done

clean:
		@rm -f *.aux *.bbl *.blg *.loa *.lof *.log *.lot *.out *.toc
		@rm -f *.pdf $(TARGETS:.pdf=.dvi) $(TARGETS:.pdf=.ps) *.tmp

depend:
		@mv Makefile Makefile.bak && \
		sed -e '/^# dependencies/,$$ d' Makefile.bak > Makefile && \
		rm -f Makefile.bak && echo '# dependencies' >> Makefile
		@for TARGET in $(TARGETS:.pdf=); do \
		    set -- $$TARGET.tex; \
		    while [ $$# -gt 0 ]; do \
			for dependency in `sed -n $(DEPEND) $$1`; do \
			    echo $$dependency; \
			    case $$dependency in \
				*.bst)  dependency=`kpsewhich $$dependency`; \
					echo $$TARGET.pdf: $$TARGET.bbl; \
					echo $$TARGET.dvi: $$TARGET.bbl; \
					echo $$TARGET.bbl: $$dependency;; \
				*.bib)  dependency=`kpsewhich $$dependency`; \
					echo $$TARGET.bbl: $$dependency;; \
				*.cls)  dependency=`kpsewhich $$dependency`; \
					echo $$TARGET.pdf: $$dependency; \
					echo $$TARGET.dvi: $$dependency;; \
				*.sty)  dependency=`kpsewhich $$dependency`; \
					echo $$TARGET.pdf: $$dependency; \
					echo $$TARGET.dvi: $$dependency;; \
				*.tex)  dependency=`kpsewhich $$dependency`; \
					echo $$TARGET.pdf: $$dependency; \
					echo $$TARGET.dvi: $$dependency; \
					set -- $$* $$dependency;; \
				*)      echo $$TARGET.pdf: $$dependency; \
					echo $$TARGET.dvi: $$dependency;; \
			    esac >> Makefile; \
			done; \
			shift; \
		    done; \
		done


# dependencies
