# CSC1034: Project 3

This package is built as a part of CSC1034: Project 3.

## Introduction
I implemented the PageRank algorithm developed which manages to put relevant websites at the top of the search 
results. We can estimate PageRank through random walkers or through probability distribution.

Type `python page_rank.py school_web.txt` to run stochastic_page_rank.

Type `python page_rank.py -m=distribution school_web.txt` to run distribution_page_rank.

Type `python page_rank.py -r=100000 -s=10 -n=30 school_web.txt` to run stochastic_page_rank with 100000 repeats
and 10 steps that displays the top 30 websites.
