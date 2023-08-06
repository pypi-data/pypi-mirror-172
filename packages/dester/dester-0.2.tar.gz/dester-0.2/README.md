# dester-linter

## Description
A linter for LaTeX files.

## How to install
pip install dester

## How to use
The command is run as a command-line tool: "dexter-linter filename".\
Arguments:\
filename - path to the file you want to execute the linter on.
Excepted file extenstions are .tex, .bib, .tikz.

Options:\
--comment=int - passes how many spaces should be inserted after a comment sign;\
--newline=bool - if False is passed the new line will not be inserted after a sentence;\
--indent=int - how many spaces should be inserted at the beginning of the line within a block;\
--blank_lines=int - how many blank lines should be inserted before section/chapter etc.\
--overwrite=bool - to overwrite the input file.\

Default values:\
--comment=1 - one space is inserted after a comment sign;\
--newline=True - a newline is inserted after a sentence;\
--indent=4 - four spaces are inserted at the beginning of a line within a begin{item}\end{item} block;\
--blank_lines=1 - one blank line is inserted before section\subsection\subsubsection\chapter\paragraph\subparagraph.\
--overwrite=False - a new outpur file is created in the same folder.

## Licence
MIT License