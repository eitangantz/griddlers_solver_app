# griddlers_solver_app
This app solves griddlers using Genetic Algorithms.
</br>
![ezgif com-gif-maker](https://user-images.githubusercontent.com/50427111/128092108-9220080f-1513-4b6e-9a9c-603085b55b06.gif)

</br>

use python 3.7 or above.
</br>
to run the app use the command: python griddlers_solver.py --input flower2.txt
</br>
--input - the input file which contains the constraints for the griddler.
</br>
--Popsize - the size of the population. default value is 100.
</br>
--Method - the type of the algorithm (1: for the regular, 2:for the lamarckian, 3: for darwin).default is 1.
</br>

the input file is 50 lines long.
</br>
the first 25 lines are the constraints for the 25 columns(from left to right).
</br>
the next 25 lines are the constraints for the 25 rows(from top to bottom).
</br>
</br>
every 50 generations the best solution found so far will be presented.


<b>input file example<b/>:

input.txt:
</br>
3
</br>
2 2
</br>
1 1
</br>
2 2
</br>
3
</br>
3
</br>
2 2
</br>
1 1
</br>
2 2
</br>
3
</br>
the corresponding  griddler:
</br>

![alt text](https://github.com/eitangantz/griddlers_solver_app/blob/master/image.png)





