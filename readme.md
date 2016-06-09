Visualizing UW Course Prerequisite Sequences
===============

## Team Members

1. [Dylan Babbs (dbabbs)](mailto:dbabbs@uw.edu)
2. [Jordan Starkey (jds56)](mailto:jds56@uw.edu)

## Project

Navigating the UW course catalog can be a difficult task -- especially when dealing with prerequisites. The course description lists the prerequisites necessary in order to enroll in a specific course, however, the description lists only the first degree of prerequisites required. For example, CSE 373: Data Structures and Algorithms, lists CSE 143 as the only required prerequisite. Unbeknownst to a student browsing the catalog, CSE 143 requires CSE 142 as a prerequisite. Therefore, the prerequisites needed to enroll in CSE 373 are both CSE 142 and CSE 143.

Coursework planning can become a headache within minutes of browsing the catalog. The goal of this tool is to improve degree and coursework planning transparency by providing an intuitive visualization experience using trees. All the user is required to do is input a course in order to explore courses series. The user’s course input becomes the node of the tree, and the node’s children become the “post”-requisites of the course. Without this tool, students are forced to backwards trace their course sequences to find course’s second (or higher) degree prerequisites.

[Poster](http://cse512-16s.github.io/fp-dbabbs-jordanstarkey95/poster-dbabbs-jds56.pdf) | 
[Final Paper](http://cse512-16s.github.io/fp-dbabbs-jordanstarkey95/paper-dbabbs-jds56.pdf) |
[Progress Presentation Deck](http://cse512-16s.github.io/fp-dbabbs-jordanstarkey95/slides-dbabbs-jds56.pdf)


![alt text](http://cse512-16s.github.io/fp-dbabbs-jordanstarkey95/summary.png "Project")

## Breakdown

A breakdown of how the work was split among the group members and a commentary on the research/development process.

---- If you decide not to put these info in the project page put them down here -----

## Running Instructions

Put your running instructions here.  (Tell us how to open your visualization.)

Access our visualization at http://cse512-16s.github.io/fp-dbabbs-jordanstarkey95/ or download this repository and run `python -m SimpleHTTPServer 8888` and access this from http://localhost:8888/.
