# griddlers_solver_app
use python 3.7 or above.
to run the app use the command: python griddlers_solver.py --input flower2.txt

--input - the input file which contains the constraints for the griddler. i gave 3 input file examples.
--Popsize - the size of the population. default value is 100.
--Method - the type of the algorithm (1: for the regular, 2:for the lamarckian, 3: for darwin).default is 1.

the input file is 50 lines long.
the 25 first lines are the constraints for the 25 columns(from left to right).
the next 25 lines are the constraints for the 25 rows(from top to bottom).

for example:

File.txt:
3
2 2
1 1
2 2
3
3
2 2
1 1
2 2
3

![alt text](https://drive.google.com/file/d/10P86njS3IV2Trc9-S7knaT6RE349T3h1/view?usp=sharing)


every 50 generations the best solution founded so far will be presented.
