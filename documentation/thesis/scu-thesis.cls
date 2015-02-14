% scu-thesis.cls
% vim:filetype=tex
%
% Darren C. Atkinson (datkinson@scu.edu)
%
% I make no claim that this format actually corresponds to any official SCU
% thesis format because, as far as I know, there is no official format.
%
% Like most LaTeX classes, this class does not set the font or font size.
% However, most options to the report class including 10pt, 11pt, and 12pt
% are accepted.
%
% 6/2/2009  - Initial version
% 10/1/2013 - Increased width of signature lines.
%             Added support for multiple authors, department, and degrees
%             Thanks to Collin Lee for the initial redesign.

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{scu-thesis}[2013/10/01 SCU Thesis class]

\DeclareOption{landscape}{\OptionNotUsed}
\DeclareOption{twocolumn}{\OptionNotUsed}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax
\LoadClass{report}
\RequirePackage{setspace}


% A 1in margin on all sides seems reasonable, plus a little bit of extra on
% one side for binding.  An official copy of a thesis shouldn't be printed
% two-sided, but I can see printing a two-sided copy for yourself, so the
% binding offset is separate from the left margin (since in a two-sided
% document it would be part of the right margin).

\newlength{\@margintop}
\setlength{\@margintop}{1.0in}

\newlength{\@marginbottom}
\setlength{\@marginbottom}{1.0in}

\newlength{\@marginleft}
\setlength{\@marginleft}{1.0in}

\newlength{\@marginright}
\setlength{\@marginright}{1.0in}

\newlength{\@bindingoffset}
\setlength{\@bindingoffset}{0.5in}


% \textwidth = \paperwidth - \@marginleft - \@marginright - \@bindingoffset

\setlength{\textwidth}{\paperwidth}
\addtolength{\textwidth}{-\@marginleft}
\addtolength{\textwidth}{-\@marginright}
\addtolength{\textwidth}{-\@bindingoffset}


% \textheight = \paperheight - \@margintop - \@marginbottom

\setlength{\textheight}{\paperheight}
\addtolength{\textheight}{-\@margintop}
\addtolength{\textheight}{-\@marginbottom}


% \evensidemargin = \@marginleft - 1in
% \oddsidemargin = \@marginleft + \@bindingoffset - 1in

\setlength{\evensidemargin}{\@marginleft}
\addtolength{\evensidemargin}{-1in}
\setlength{\oddsidemargin}{\evensidemargin}
\addtolength{\oddsidemargin}{\@bindingoffset}


% \topmargin = \@margintop - \headheight - \headsep - 1in

\setlength{\topmargin}{\@margintop}
\addtolength{\topmargin}{-\headheight}
\addtolength{\topmargin}{-\headsep}
\addtolength{\topmargin}{-1in}


% \marginparwidth = \@marginright - \marginparsep

\setlength{\marginparwidth}{\@marginright}
\addtolength{\marginparwidth}{-\marginparsep}


% Switch to single spacing in the chapter title.

\let\@oldchap\chapter
\newcommand{\@schap}[1]{\def\baselinestretch{1}\@oldchap*{#1}}
\newcommand{\@chap}[2][]{\def\baselinestretch{1}\@oldchap[#1]{#2}}
\renewcommand*{\chapter}{\secdef{\@chap}{\@schap}}


% Each use of \author, \degree, or \department adds to the list.  Actually,
% since LaTeX doesn't have array variables, each use creates a new variable
% with a common prefix.  They will be listed in the order added.

\newcommand{\degreeword}{\ifnum\the@degreecount>1 degrees\else degree\fi}

\newcounter{@authorcount}
\renewcommand{\author}[1]{\stepcounter{@authorcount}%
\expandafter\def\csname @author\the@authorcount\endcsname{#1}}

\newcounter{@degreecount}
\newcommand{\degree}[1]{\stepcounter{@degreecount}%
\expandafter\def\csname @degree\the@degreecount\endcsname{#1}}

\newcounter{@departmentcount}
\newcommand{\department}[1]{\stepcounter{@departmentcount}%
\expandafter\def\csname @department\the@departmentcount\endcsname{#1}}

\newcounter{@itemcount}
\newcommand{\@tableof}[2][]{{\setcounter{@itemcount}{0}%
\newcommand{\recurse}{\ifnum\value{@itemcount}<\value{@#2count}%
\stepcounter{@itemcount}#1{\csname @#2\the@itemcount\expandafter\endcsname}\\%
\recurse\fi}\begin{tabular}{c}\recurse\end{tabular}}}


% \frontmatter produces the unnumbered signature page and sets the page
% numbering.  It should be the first command used in the document.

\newcommand{\frontmatter}{
\cleardoublepage
\thispagestyle{empty}
\renewcommand{\thepage}{\roman{page}}
\renewcommand{\contentsname}{Table of Contents}
\begin{center}
\textbf{\Large SANTA CLARA UNIVERSITY} \\
\vspace{1mm}
\textbf{\@tableof[\MakeUppercase]{department}} \\
\vspace{8mm}
\hfill Date: \@date \\
\vspace{8mm}
I HEREBY RECOMMEND THAT THE THESIS PREPARED UNDER MY SUPERVISION BY \\
\vspace{8mm}
\textbf{\@tableof{author}} \\
\vspace{8mm}
ENTITLED \\
\vspace{8mm}
\textbf{\Large\@title} \\
\vspace{16mm}
BE ACCEPTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE
\MakeUppercase{\degreeword} OF \\
\vspace{8mm}
\@tableof[\MakeUppercase]{degree}
\end{center}
\vspace{8mm}
}


% \signature adds a labeled signature line and can be used multiple times.

\newcommand{\@signaturewidth}{70mm}

\newcommand{\signature}[1]{
\vspace*{8mm}
\begin{flushright}
\begin{minipage}{\@signaturewidth}
\hrulefill \\
\centering #1
\end{minipage}
\end{flushright}
}


% \maketitle has been changed to produce an unnumbered, separate title page.

\renewcommand{\maketitle}{
\newpage
\thispagestyle{empty}
\begin{center}
\vspace*{40mm}
\textbf{\Large\@title} \\
\vspace{15mm}
by \\
\vspace{15mm}
\@tableof{author} \\
\vspace{40mm}
Submitted in partial fulfillment of the requirements \\
for the \degreeword\ of \\
\@tableof{degree} \\
School of Engineering \\
Santa Clara University \\
\vfill
Santa Clara, California \\
\@date
\end{center}
}


% The abstract environment has also been changed to produce a separate,
% unnumbered abstract page with the title and author information.

\renewenvironment{abstract}{
\newpage
\thispagestyle{empty}
\begin{center}
\textbf{\Large\@title} \\
\vspace{8mm}
\@tableof{author} \\
\vspace{8mm}
\@tableof{department} \\
Santa Clara University \\
\@date \\
\vspace{10mm}
ABSTRACT
\end{center}
}{\newpage}


% \mainmatter resets the page numbering and enables double spacing.  It
% should be used before the start of the introduction.

\newcommand{\mainmatter}{
\cleardoublepage
\setcounter{page}{1}
\renewcommand{\thepage}{\arabic{page}}
\doublespacing
}


% \backmatter resets single spacing, and should be used before the
% bibliography or appendices.

\newcommand{\backmatter}{
\clearpage\singlespacing
}
