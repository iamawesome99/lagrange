# Lagrange

What can I say?
It's a python program that displays a variable number of points on a screen,
and from them calculates and displays the corresponding Lagrange polynomial (https://en.wikipedia.org/wiki/Lagrange_polynomial#Examples).

It uses matplotlib to do displaying *and* interactivity.
Ain't that just cool?

---

# Files

main.py holds most of the main code:
 - Lagrange polynomial calculation (for the most part)
 - Matplotlib plotting and animations.
 
polynomial.py holds some code dedicated to doing calculations on polynomials.
It is designed to be reused in other projects, so it's a bit overkill for this project.

---

# Running

Download the files, install the requirements.txt packages, and run main.py!
Changing the number of dots means changing a variable in main.py. 
Will work on that soon.