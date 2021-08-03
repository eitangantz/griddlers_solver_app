from tkinter import *
from tkinter.font import Font
import sys
import random
import time
import matplotlib.pyplot as plt
import math
import argparse


board = [[0 for i in range(25) ] for j in range(25)]

def configure_window(width=200, height=200):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_pos = screen_width // 2 - width // 2
    y_pos = screen_height // 2 - height // 2
    root.geometry("{0}x{1}+{2}+{3}".format(width, height, x_pos, y_pos - 14)) 
def paint_nonogram(rows, columns,rowsConstraints,columnsConstraints,bestSolution):
    for i in range(rows):
        for j in range(columns):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                c = []
                for k in range(len(columnsConstraints[j-1])):
                    if columnsConstraints[j-1][k] != 0:
                        c.append(columnsConstraints[j-1][k])
                    else:
                        c.insert(0,columnsConstraints[j-1][k])
                lbl_frm = Frame(main_frm, width=22.5, height=110, borderwidth=1, relief="solid")
                lbl = Label(lbl_frm, text=c, font=font, wraplength=16)
                lbl.place(relx=.5, rely=.5, anchor='c')
                lbl_frm.grid(row=i , column=j)
            elif j == 0:
                r = []
                for k in range(len(rowsConstraints[i-1])):
                    if rowsConstraints[i-1][k] != 0:
                        r.append(rowsConstraints[i-1][k])
                    else:
                        r.insert(0,rowsConstraints[i-1][k])
                lbl_frm = Frame(main_frm, width=110, height=22.5, borderwidth=1, relief="solid")
                lbl = Label(lbl_frm, text=r, font=font)
                lbl.place(relx=.5, rely=.5, anchor='c')
                lbl_frm.grid(row=i , column=j)
            else:
                if bestSolution[i-1][j-1] == 0:
                    lbl_frm = Frame(main_frm, width=22.5, height=22.5, borderwidth=1, relief="solid",bg="white")
                if bestSolution[i-1][j-1] == 1:
                    lbl_frm = Frame(main_frm, width=22.5, height=22.5, borderwidth=1, relief="solid",bg="green")
                lbl_frm.grid(row=i , column=j)
                board[i-1][j-1] = (lbl_frm)
    


def update_ui(bestSolution):
    for i in range(25):
        for j in range(25):
            if bestSolution[i][j] == 0:
                board[i][j].config(bg="white")
            if bestSolution[i][j] == 1:
                board[i][j].config(bg="green")

            root.update()           


def input_to_constraints(filePath):
    rowsConstraints=[]
    columnsConstraints = []
    # Using readlines()
    file1 = open(filePath, 'r')
    Lines = file1.readlines()
    count = 0
    # Strips the newline character
    i=0
    for line in Lines:
        line.strip()
        if i<25:
            c = [int(s)for s in line.split(" ")]
            c.reverse()
            if len(c)<8:
                for j in range(8-len(c)):
                    c.append(0)
            columnsConstraints.append(c)
        else:
            c = [int(s)for s in line.split(" ")]
            c.reverse()
            if len(c)<8:
                for j in range(8-len(c)):
                    c.append(0)
            rowsConstraints.append(c)
        i+=1
    return rowsConstraints, columnsConstraints

#second approach: generate solutions that fit the row conditions:
def get_permutations(rowC,rowsize):
    #first condition:
    blocks = [1]*(rowC[0])
    #check if only one condition is in the row
    if len(rowC) == 1 or rowC[1] == 0:
        perms = []
        for i in range(rowsize - rowC[0] + 1):
            prev = [0]*i
            after = [0]*(rowsize - i - rowC[0])
            perms.append(prev + blocks + after)
        return perms
    perms = []
    for i in range(rowC[0], rowsize):
        for p in get_permutations(rowC[1:], rowsize - i - 1):
            prev = [0]*(i - rowC[0])
            perms.append(prev + blocks + [0] + p)
    return perms

def get_random_row(row_num,perms):
        return random.choice(perms[row_num])

def create_first_generation(population_size,perms,rowsize):
    firstGeneration = []
    for i in range(population_size):
        randSol = []
        for j in range (rowsize):
            randSol.append(get_random_row(j,perms))

        firstGeneration.append(randSol)
    return firstGeneration


def mutate(selection_after_cross,perms,prec,prec2):
    for sol in selection_after_cross:
        if random.randint(0,100) < prec2:
            for i in range(len(sol)):
                if random.randint(0,100) < prec:
                    sol[i] = get_random_row(i,perms)
    return selection_after_cross


def calculate_fitness(current_generation, rowConditions, columnsConstraints):

    def calculate_distance(solution,columnsConstraints):
        z=0
        sumOfmatches = 0
        for i in range(25):
            isPrevBlack = False
            counter = 0
            blackSequences = []
            for j in range(25):
                if solution[j][i] == 1 and isPrevBlack:
                    counter = counter + 1
                    isPrevBlack = True
                elif solution[j][i] == 1 and not isPrevBlack:
                    counter = 1
                    isPrevBlack = True
                elif solution[j][i] == 0 and not isPrevBlack:
                    isPrevBlack = False
                elif solution[j][i] == 0 and isPrevBlack:
                    isPrevBlack = False
                    blackSequences.append(counter)
                    counter = 0

            if counter > 0:
                blackSequences.append(counter)

            #pad blackSequences with zeros if needed:
            num_of_black_sequences = len(blackSequences)
            if len(blackSequences)<8:
                for t in range(8-len(blackSequences)):
                    blackSequences.append(0)
            #compare black sequences with the row conditions and count how many of them match:
            k=0
            matches = 0
            for condition in columnsConstraints[z]:
                diff = abs(condition - blackSequences[k])
                matches = matches + diff
                k += 1
            matches = -matches
            # in case black sequences length is greater than 8:
            if len(blackSequences)>8:
                matches = matches - (len(blackSequences)-8)

            if matches == 0:
                matches += 1
            sumOfmatches += matches
            z += 1
        return sumOfmatches

    fitnessGrades = []  
    i=0
    for solution in current_generation:
        grade = calculate_distance(solution,columnsConstraints)
        fitnessGrades.append(grade)
        i+=1
    
    return fitnessGrades


def select(previousGeneration,grades,scale):
    #create dic:
    dic = {}
    z=0
    size_of_dic = len(previousGeneration)
    for sol in previousGeneration:
        dic[grades[z]] = sol
        z+=1

    dic = dict(sorted(dic.items(), reverse = True))
    #make selection:
    selection = []
    for i in range(int(len(selection)*0.01)):
        selection.append((list(dic.keys())[j],list(dic.values())[j]))

    selection_size = len(selection)
    j=1
    for i in range(len(previousGeneration) - selection_size):
        survived_index = trunc_exp(len(dic)-1,scale)
        selection.append((list(dic.keys())[survived_index],list(dic.values())[survived_index]))

    selection.sort(reverse=True)

    selection1 = []
    for p in selection:
        selection1.append(p[1])

    return selection1


#lamarck
def optimize(generation,perms,rowsConstraints,columnsConstraints):
    for sol in generation:
        solVariations = []
        copy = copy_solution(sol)
        #create 2 copies of the original sol
        for i in range(2):
            originalSolCopy = copy_solution(sol)
            solVariations.append(originalSolCopy)
        solVariations = mutate(solVariations,perms,10,100)
        solVariations.append(copy)
        grades = calculate_fitness(solVariations,rowsConstraints,columnsConstraints)
        best, indexOfBest = best_fit(grades)
        sol = solVariations[indexOfBest]
#darwin
def get_copy_optimize(firstGeneration,perms,rowsConstraints,columnsConstraints):
    copyOptimizedGeneration = []
    for sol in firstGeneration:
        solVariations = []
        copy = copy_solution(sol)
        #create 2 copies of the original sol
        for i in range(2):
            originalSolCopy = copy_solution(sol)
            solVariations.append(originalSolCopy)

        solVariations = mutate(solVariations,perms,10,100)
        solVariations.append(copy)
        grades = calculate_fitness(solVariations,rowsConstraints,columnsConstraints)
        best, indexOfBest = best_fit(grades)
        copyOptimizedGeneration.append(solVariations[indexOfBest])
    return copyOptimizedGeneration

def copy_solution(sol):
    copy = []
    for row in sol:
        copy.append(row)
    return copy



def crossover(selection):
    slectionAfterCross = []
    for j in range(int(len(selection)*0.01)):
        slectionAfterCross.append(selection[j])
    size = len(slectionAfterCross)
    for i in range(len(selection) - size):
        if random.randint(0,4) == 1: #50% first technique
            if random.randint(0,100) < 90:
                    sol1 = selection[random.randint(0,len(selection)-1)]
                    sol2 = selection[random.randint(0,len(selection)-1)]
                    randArray = [0]*25
                    for bit in randArray:
                        if random.randint(0,1) == 1:
                            bit = 1
                    k = 0
                    offspring = []
                    for bit in randArray:
                        if bit == 1:
                            offspring.append(sol1[k])
                        else:
                            offspring.append(sol2[k])
                        k+=1
                    slectionAfterCross.append(offspring)
            else:
                slectionAfterCross.append(selection[i])
        else: #50% second technique
            if random.randint(0,100) < 90:
                pos = random.randint(0,25-1)
                sol1 = selection[random.randint(0,len(selection)-1)]
                sol2 = selection[random.randint(0,len(selection)-1)]
                offspring = []
                for row in sol1[:pos]:
                    offspring.append(row)
                for row in sol2[pos:]:
                    offspring.append(row)
                slectionAfterCross.append(offspring)
            else:
                slectionAfterCross.append(selection[i])
    return slectionAfterCross


def best_fit(grades):
    best = max(grades)
    bestIndex = grades.index(best)
    return best, bestIndex

def average(grades):
    return sum(grades) / len(grades)

def worst(grades):
    return min(grades)

def loop(firstGeneration,rowsConstraints,columnsConstraints,method):
    m = 5
    scale = 0.1
    epoch = 1
    bestGradeCurrentGeneration = 0
    gradesForPlot = []
    epochForPlot = []
    bestForPlot = []
    worstForPlot = []
    bestGradeSoFar = -200
    bestSolutionSoFar = copy_solution(firstGeneration[0])
    prev = -200
    while True:

        if epoch % 500 == 0:
            print("number of satisfied columns: " + str(get_num_satisfied_columns(bestSolutionSoFar,columnsConstraints)))
            print("best solution score: " + str(bestGradeSoFar))
            print("average score: " + str(gradesForPlot[len(gradesForPlot)-1]))
            print("worst score: " + str(worstForPlot[len(worstForPlot)-1]))
            print("epoch: " + str(epoch))
            update_ui(bestSolutionSoFar)
            time.sleep(1)
            #print("plotting:")
            #plt.plot(epochForPlot, gradesForPlot)
            #plt.plot(epochForPlot, bestForPlot)
            #plt.plot(epochForPlot, worstForPlot)
            #plt.legend(['y = average', 'y = best', 'y = worst'], loc='upper left')    
            #plt.show()
            if prev >= bestGradeCurrentGeneration:
                print("handle converge")
                firstGeneration = mutate(newCrossover,perms,20,100) #approach 2               
            prev = bestGradeCurrentGeneration

        if epoch ==20000:
            break


        if epoch % 50 == 0:
            gradesForPlot.append(average(grades))
            bestForPlot.append(bestGradeCurrentGeneration)
            worstForPlot.append(worst(grades))
            epochForPlot.append(epoch)
            update_ui(bestSolutionSoFar)

        if method == 3: #darwin
            #display results by optimization
            copyOptimizedGeneration = get_copy_optimize(firstGeneration,perms,rowsConstraints,columnsConstraints)
            grades = calculate_fitness(copyOptimizedGeneration,rowsConstraints,columnsConstraints)
            bestGradeCurrentGeneration, indexOfBest = best_fit(grades)
            print(bestGradeCurrentGeneration)
            if bestGradeCurrentGeneration >= bestGradeSoFar:
                bestGradeSoFar = bestGradeCurrentGeneration
                bestSolutionSoFar = copy_solution(copyOptimizedGeneration[indexOfBest])
            bestSolutionLastGeneration = copy_solution(copyOptimizedGeneration[indexOfBest])
            #select from the solutions before the optimization 
            newSelection = select(firstGeneration,grades,scale) 
            newCrossover = crossover(newSelection) 
            nextGeneration = mutate(newCrossover,perms,m,100) #approach 2
            firstGeneration = nextGeneration
            epoch+=1
            continue

        grades = calculate_fitness(firstGeneration,rowsConstraints,columnsConstraints)
        bestGradeCurrentGeneration, indexOfBest = best_fit(grades)
        print(bestGradeCurrentGeneration)
        if bestGradeCurrentGeneration >= bestGradeSoFar:
            bestGradeSoFar = bestGradeCurrentGeneration
            bestSolutionSoFar = copy_solution(firstGeneration[indexOfBest])
        bestSolutionLastGeneration = copy_solution(firstGeneration[indexOfBest])

        if method == 2: #lamarck
            optimize(firstGeneration,perms,rowsConstraints,columnsConstraints)

        newSelection = select(firstGeneration,grades,scale) #approach 2
        newCrossover = crossover(newSelection) #approach 2
        nextGeneration = mutate(newCrossover,perms,m,100) #approach 2
        firstGeneration = nextGeneration
        epoch+=1


def get_num_satisfied_columns(solution,columnsConstraints):
    z=0
    satisfiedColumns = 0
    for i in range(25):
        isPrevBlack = False
        counter = 0
        blackSequences = []
        for j in range(25):
            if solution[j][i] == 1 and isPrevBlack:
                counter = counter + 1
            elif solution[j][i] == 1 and not isPrevBlack:
                counter = 1
                isPrevBlack = True
            elif solution[j][i] == 0 and not isPrevBlack:
                isPrevBlack = False
            elif solution[j][i] == 0 and isPrevBlack:
                isPrevBlack = False
                blackSequences.append(counter)
                counter = 0

        if counter > 0:
            blackSequences.append(counter)

        #pad blackSequences with zeros if needed:
        num_of_black_sequences = len(blackSequences)
        if len(blackSequences)<8:
            for t in range(8-len(blackSequences)):
                blackSequences.append(0)
        #compare black sequences with the row conditions and count how many of them match:
        k=0
        matches = 0
        for condition in columnsConstraints[z]:
            if condition ==  blackSequences[k]:
                matches = matches + 1
            k += 1
        # in case black sequences length is greater than 8:
        if len(blackSequences)>8:
            matches = matches - (len(blackSequences)-8)
        if matches == 8:
            satisfiedColumns += 1
        z += 1
    return satisfiedColumns

def trunc_exp(upper_bound, scale_param = 0.1):
    upper_bound = float(upper_bound) + 1.0 - sys.float_info.epsilon
    trunc = 1.0 - math.exp(-1.0 / scale_param)
    return int((-upper_bound * scale_param) * math.log(1.0 - trunc * random.random()))


root = Tk()
root.title("Griddlers")
main_frm = Frame(root)
main_frm.place(relx=.5, rely=.5, anchor='c')
font = Font(family="Courier New",size=8)


parser = argparse.ArgumentParser()
parser.add_argument('--input',type=str,required = True)
parser.add_argument('--popsize',default=100,type=int)
parser.add_argument('--method',default=1,type=int)
args, unknown = parser.parse_known_args()

rowsConstraints, columnsConstraints = input_to_constraints(args.input)

populationSize = args.popsize
method = args.method


perms = []
for i in range(25):
    perms.append(get_permutations(rowsConstraints[i],25))


firstGeneration = create_first_generation(populationSize,perms,25) 

grades = calculate_fitness(firstGeneration,rowsConstraints,columnsConstraints)
bestGradeCurrentGeneration, indexOfBest = best_fit(grades)
bestSolutionLastGeneration = firstGeneration[indexOfBest]
paint_nonogram(25+1, 25+1,rowsConstraints, columnsConstraints, bestSolutionLastGeneration)
configure_window(750, 750)
newSelection = select(firstGeneration,grades,0.1) 
newCrossover = crossover(newSelection) 
secondGeneration = mutate(newCrossover,perms,4,100)

update_ui(secondGeneration[0])

root.after(3000, loop(secondGeneration,rowsConstraints,columnsConstraints,args.method))
root.mainloop()