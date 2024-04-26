import subprocess
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from copy import deepcopy


dnum = {}

def croisement(ile1, ile2, ile3, ile4):
    """
    ile_x = (i_x, j_x) # couple
    cette fonction retourne Vrai si: Le Pont (ile1, ile2) se croise avec le Pont (ile3, ile4)
    """
    i1,j1 = ile1
    i2,j2 = ile2
    i3,j3 = ile3
    i4,j4 = ile4

    if ile1 == ile3 or ile1 == ile4 or ile2 == ile3 or ile2 == ile4:
        return False                      
    
    if i1 == i2 and j1 != j2 and j3 == j4 and i3 != i4: # (ile1, il2) est horizental et (ile3, ile4) est vertical
        if ((j3 > j1 and j3 < j2) or (j3 > j2 and j3 < j1)) and ((i3 < i1 and i4 > i1) or (i4 < i1 and i3 > i1)):
            return True
        else:
            return False
        
    elif j1 == j2 and i1 != i2 and i3 == i4 and j3 != j4: # (ile1, il2) est vertical et (ile3, ile4) est horizental
        if ((i3 > i1 and i3 < i2) or (i3 > i2 and i3 < i1)) and ((j3 < j1 and j4 > j1) or (j4 < j1 and j3 > j1)):
            return True
        else:
            return False
        
    else:
        return False
    

def ponts_possibles_croisement(grid):
    listeClauses = ""
    for ile1 in grid.keys():
        for ile2 in grid[ile1][3]:
            for ile3 in grid.keys():
                for ile4 in grid[ile3][3]:
                    if croisement((grid[ile1][1], grid[ile1][0]),(grid[ile2][1], grid[ile2][0]), (grid[ile3][1], grid[ile3][0]), (grid[ile4][1], grid[ile4][0])):
                        if "(" + "(" + ile3 + ile4 + "+" + ile4 + ile3 +")" + "<>" +  "(" + ile1 + ile2 + "+" + ile2 + ile1 + ")" + ")" not in listeClauses:
                            listeClauses += "(" + "(" + ile1 + ile2 + "+" + ile2 + ile1 +")" + "<>" +  "(" + ile3 + ile4 + "+" + ile4 + ile3 +")"+")" + "."

    return listeClauses[0:len(listeClauses)-1]


def chemin(d):
    res = []

    def rec_chemin(d,l,sommets):
        if d[sommets[-1]][3] == []:
            for i in d.keys():
                if i in sommets and d[i][3] != []:
                    for j in d[i][3]:
                        if j not in sommets:
                            sommet1 = deepcopy(sommets)
                            l1 = deepcopy(l)
                            l1[-1]+="."+ "(" + j + i + "+" + i + j + ")"
                            dcpy = deepcopy(d)
                            dcpy[i][3].remove(j)
                            dcpy[j][3].remove(i)
                            if len(sommet1) == len(d.keys()) - 1:
                                res.append("("+l1[0]+")")
                            else:
                                rec_chemin(dcpy, l1, sommet1 + [j])
            return

        min_rec = False
        sommet1 = deepcopy(sommets)
        for i in d[sommets[-1]][3]:
            if i in sommets:
                continue
            min_rec = True
            l1 = deepcopy(l)
            l1[-1]+="."+ "(" + i + sommets[-1] + "+" + sommets[-1] + i + ")"
            dcpy = deepcopy(d)
            dcpy[sommets[-1]][3].remove(i)
            dcpy[i][3].remove(sommets[-1])
            if len(sommet1) == len(d.keys()) - 1:
                res.append("("+l1[0]+")")
            else:
                rec_chemin(dcpy, l1, sommet1 + [i])
        if not min_rec:
            dcpy = deepcopy(d)
            dcpy[sommets[-1]][3] = []
            rec_chemin(dcpy,l,sommets)
        return     

    for j in d.keys():
        for i in d[j][3]:
            sommets = [j, i]
            l = []
            l.append("("+j+i+"+"+i+j+")")
            dcpy = deepcopy(d)
            dcpy[j][3].remove(i)
            dcpy[i][3].remove(j)
            rec_chemin(dcpy, l, sommets)
    return res


def func_combinaisons(d):
    """
    d:dict(grille)
    return la liste des clauses en str
    """
    global dnum
    res = []
    l=len(d.keys())
    res1=""
    for j in d.keys():
        cl=dist(j,d[j][2],d[j][3])
        cl2=tr_num(cl)
        res.append(cl2)
        cl1=[]
        #print(f"POUR LE POINT {j}")
        for v in cl:
            #print(v)
            cl1.append("("+".".join(v)+")")
        temp="("+"+".join(cl1)+")"
        #print(temp)
        res1=res1+temp+"."
    return res1[0:len(res1)-1]
    
        

def dist(pt,deg,lpos):
    """
    return la partition des ensembles possibles de taille deg pour pt
    """
    l=[]
    for i in lpos:
        l.append(pt+i)
        l.append(i+pt)
    t=[]
    for i in l:
        t.append([i])
    if deg==1:    
        t1 = []
        for i in l:
            tmp = [i]
            for j in l:
                if i != j:
                    tmp.append("-"+j)
            t1.append(tmp)  
 
        return t1
    res1=rec_dist(l,t,deg-1)
    res2 = deepcopy(res1)
    for i in range(len(res1)):
        tempi = deepcopy(res1[i])
        for j in range(len(res1)):
            if i != j:
                for k in res1[j]:
                    if k not in res1[i] and "-"+k not in tempi:
                        tempi.append("-"+k)
        res2[i] = tempi
    
    return res2

def rec_dist(ens,enc,deg):
    """
    return les listes en construction de la distribution
    """
    if deg==0:
        return enc
    t=[]
    for i in enc:
        for j in ens:
            if j not in i and ens.index(j)>ens.index(i[-1]):
                k=i+[j]
                t.append(k)
    return rec_dist(ens,t,deg-1)

def tr_num(l):
    global dnum
    res=[]
    for i in l:
        temp=[]
        for j in i:
            k = j
            if "-" in k:
                k = k.replace("-", "")
            if k in dnum.keys():
                temp.append("-"+dnum[k])
            else:
                dnum[k]=str(len(dnum.keys())+1)
                temp.append(dnum[k])
        res.append(temp)
    return res

def tr_num1(s):
    global dnum
    for i in dnum.keys():
        s=s.replace(i,dnum[i])
    return s


def tr_num2(s):
    global dnum
    l = list(dnum.keys())
    for i in l[::-1]:
        s = s.replace(dnum[i], i)
    return s

def transform_sol_to_bridges(sol):
    #turn solution into array
    sol = sol.split(" ")
    #remove non bridges(ex: -AB)
    sol_clean = []
    for bridge in sol:
        if len(bridge)>0:
            if bridge[0] != "-":
                bridge = sorted(bridge)
                #turn into hashable
                bridge=''.join(bridge)
                bridge+=str(1)
                sol_clean += [bridge]
    #check for duplicates
    sol_non_dup = []
    duplicates = []
    for bridge in sol_clean:
        if bridge not in sol_non_dup:
            sol_non_dup+=[bridge]
        else:
            duplicates.append(sol_non_dup.index(bridge))
    #increase bridge count
    sol_final = []
    for i in range(len(sol_non_dup)):
        sol_final.append(list(sol_non_dup[i]))
        if i in duplicates:
            sol_final[i][2] = "2"
    return sol_final

        
    
def solve(window,grid,size_x,size_y,size,space):

    if len(grid.keys()) >= 26:
        print("LIMIT REACHED: only 25 islands allowed")
        exit(0)

    # les 3 formules initiales
    cnff = func_combinaisons(grid)
    croisement_cnf =  ponts_possibles_croisement(grid) 
    chemins = ""
    if size_x <= 7 or size_y <= 7:
        chemins = "+".join(chemin(grid))

    # initialisation de bddc pour la formule croisement
    text_file = open("croisement_no_cnf.txt", "w")
    text_file.write("cnf ")
    text_file.write(croisement_cnf)
    text_file.write(";")
    text_file.close()

    # initialisation de bddc pour la formule croisement
    text_file = open("formule_no_cnf.txt", "w")
    text_file.write("cnf ")
    text_file.write(cnff)
    text_file.write(";")
    text_file.close()

    # initialisation de bddc pour la formule chemins
    if size_x <= 7 or size_y <= 7:
        text_file = open("formule_chemins_nocnf.txt","w")
        text_file.write("cnf ")
        text_file.write(chemins)
        text_file.write(";")
        text_file.close()

    # execution du script shell qui execute les focntions bddc
    subprocess.call(['sh','./to_cnf.sh']) #----> to run shell scripts in python

    #recuperation des resultats

    # recuperation de la formule initiale (combinaisons)
    text_file = open("formule_cnf.txt", "r")
    cnff = text_file.readline()
    text_file.close()
    cnff = cnff[0:len(cnff)-1]
    if cnff == "0":
        cnff = ""

    # recuperation de la formule des croisements
    text_file = open("croisement_cnf.txt", "r")
    croisement_cnf = text_file.readline()
    text_file.close()
    croisement_cnf = croisement_cnf[0:len(croisement_cnf)-1]

    # recuperation de la formule des chemins
    if size_x <= 7 or size_y <= 7:
        text_file = open("formule_chemins_cnf.txt", "r")
        chemins = text_file.readline()
        text_file.close()
        chemins = chemins[0:len(chemins)-1]


    if croisement_cnf != "":    
        cnff = croisement_cnf + "." + cnff

    if (size_x <= 7 or size_y <= 7) and chemins != "":
        cnff = cnff + "." + chemins

    cnff=tr_num1(cnff)

    cnff = cnff.replace(" ", "")
    cnff = cnff.replace("+", " ")
    cnff = cnff.replace(".", " 0\n")
    cnff = cnff.replace("(", "")
    cnff = cnff.replace(")", "")
    cnff = cnff + " 0"

    text_file = open("formule_cnf_input.dimacs", "w")
    text_file.write("p cnf " + str(len(dnum.keys())) + " " + str(cnff.count("\n") + 1) + "\n")
    text_file.write(cnff)
    text_file.close()
    subprocess.call(['sh','./run_minisat.sh']) #----> to run shell scripts in python
    
    text_file = open("formule_cnf.dimacs.out", "r")
    sat = text_file.readline()
    sat = sat[0:len(sat)-1]
    if sat == "SAT":
        solution = text_file.readline()
        solution = tr_num2(solution)
        solution = solution[0:len(solution)-2]
        solution = solution.replace("--", "")
        print("----> Solution: \n",solution)
        bridge_out = transform_sol_to_bridges(solution)
        visualize_grid_gout(window,grid,bridge_out,size_x,size_y,size,space)
    else:
        print("INSATISFIABLE !!!!")

    text_file.close()          

"""

GRAPHICS

"""
#Destroys current window and opens initial menu
def return_to_menu(window):
    window.destroy()
    menu()

def refresh_canvas(grid,window,size_x,size_y,size,space):
    window.destroy()
    visualize_grid_gin(grid,size_x,size_y,size,space)

#Draws Non Solved Grid
def visualize_grid_gin(grid,size_x,size_y,size,space):
    window = tk.Tk()
    window.title('Import Grid .gin')
    canvas = tk.Canvas(window,width= size_x*(space+size/2), height= size_y*(space+size/2),bg="white")
    for island in grid.keys():
        canvas.create_oval(space+grid[island][0]*space,space+grid[island][1]*space,space+(grid[island][0]*space)+size,space+(grid[island][1]*space)+size,outline="black",fill="white")
        canvas.create_text(space+grid[island][0]*space+size/2,space+grid[island][1]*space+size/2,text=grid[island][2],fill="black")
    canvas.pack()
    ttk.Label(text="Size").pack()
    scl_size = tk.Scale(from_=10,to=100,orient="horizontal")
    scl_size.set(size)
    scl_size.pack()
    ttk.Label(text="Spacing").pack()
    scl_space = tk.Scale(from_=10,to=100,orient="horizontal")
    scl_space.set(space)
    scl_space.pack()
    ttk.Button(text="Solve",command=lambda: solve(window,grid,size_x,size_y,size,space)).pack()
    ttk.Button(text="Refresh",command=lambda: refresh_canvas(grid,window,size_x,size_y,scl_size.get(),scl_space.get())).pack()
    ttk.Button(text="Return To Menu",command=lambda: return_to_menu(window)).pack()
    window.mainloop()

#Draws Solved Grid
def visualize_grid_gout(window,grid,bridges,size_x,size_y,size,space):
    window.destroy()
    window = tk.Tk()
    window.title('Import Grid .gout')
    canvas = tk.Canvas(window,width= size_x*(space+size/2), height= size_y*(space+size/2),bg="white")
    for bridge in bridges:
        if bridge[2] == "2":
            canvas.create_line(space+grid[bridge[0]][0]*space+size/4,space+grid[bridge[0]][1]*space+size/4,space+grid[bridge[1]][0]*space+size/4,space+grid[bridge[1]][1]*space+size/4,fill="black",width=5)
            canvas.create_line(space+grid[bridge[0]][0]*space+size*0.75,space+grid[bridge[0]][1]*space+size*0.75,space+grid[bridge[1]][0]*space+size*0.75,space+grid[bridge[1]][1]*space+size*0.75,fill="black",width=5) 
        else:
            canvas.create_line(space+grid[bridge[0]][0]*space+size/2,space+grid[bridge[0]][1]*space+size/2,space+grid[bridge[1]][0]*space+size/2,space+grid[bridge[1]][1]*space+size/2,fill="black",width=5)
    for island in grid.keys():
        canvas.create_oval(space+grid[island][0]*space,space+grid[island][1]*space,space+(grid[island][0]*space)+size,space+(grid[island][1]*space)+size,outline="black",fill="white")
        canvas.create_text(space+grid[island][0]*space+size/2,space+grid[island][1]*space+size/2,text=grid[island][2],fill="black")
    canvas.pack()
    ttk.Label(text="Size").pack()
    scl_size = tk.Scale(from_=10,to=100,orient="horizontal")
    scl_size.set(size)
    scl_size.pack()
    ttk.Label(text="Spacing").pack()
    scl_space = tk.Scale(from_=10,to=100,orient="horizontal")
    scl_space.set(space)
    scl_space.pack()
    ttk.Button(text="Refresh",command=lambda: refresh_canvas(grid,window,size_x,size_y,scl_size.get(),scl_space.get())).pack()
    ttk.Button(text="Return To Menu",command=lambda: return_to_menu(window)).pack()
    window.mainloop()


def read_gin(window):
    #Load file
    file_name = askopenfilename(
        filetypes=[("Grid Input File", "*.gin")]
    )
    if not file_name:
        return
    file = open(file_name, "r")
    file_content = file.read()
    file_content = file_content.splitlines()
    #init grid
    grid = {}
    grid_size = file_content[0].split(" ")
    grid_size_x = int(grid_size[0])
    grid_size_y = int(grid_size[1])
    curr_available_id = "A"

    #Load file to dict
    for j in range(1,grid_size_y+1):
        for i in range(0,grid_size_x):
            if file_content[j][i] != "0":
                grid[curr_available_id] = [i,j-1,int(file_content[j][i]),[0,0,0,0]]
                curr_available_id = chr(ord(curr_available_id)+ 1)
    #dict format

    #grid = {'1': x,y,d,[up,down,left,right],...}

    #add aligned islands
    for island in grid.keys():
        for other_island in grid.keys():
            if island != other_island:
                #Check if x1=x2
                if grid[island][0] == grid[other_island][0]:
                    #Check if y1<y2
                    if grid[island][1] < grid[other_island][1]:
                        if grid[island][3][1] == 0 or grid[other_island][1] < grid[grid[island][3][1]][1]:
                            grid[island][3][1] = other_island
                    #Check if y1>y2
                    elif grid[island][1] > grid[other_island][1]:
                        if grid[island][3][0] == 0 or grid[other_island][1] > grid[grid[island][3][0]][1]:
                            grid[island][3][0] = other_island
                #Check if y1=y2
                elif grid[island][1] == grid[other_island][1]:
                    #Check if x1<x2
                    if grid[island][0] < grid[other_island][0]:
                        if grid[island][3][3] == 0 or grid[other_island][0] < grid[grid[island][3][3]][0]:
                            grid[island][3][3] = other_island
                    #Check if x1>x2
                    elif grid[island][0] > grid[other_island][0]:
                        if grid[island][3][2] == 0 or grid[other_island][0] > grid[grid[island][3][2]][0]:

                            grid[island][3][2] = other_island
        #Filter aligned islands
        final_aligned = []
        for el in grid[island][3]:
            if el != 0:
                final_aligned+=el
        grid[island][3] = final_aligned
    file.close()
    #print(grid)
    #closes menu
    window.destroy()
    #Open Grid Visuals
    visualize_grid_gin(grid,grid_size_x,grid_size_y,20,40)
def menu():
    window = tk.Tk()
    window.title('Hashiwokakero')
    image_logo = ImageTk.PhotoImage(Image.open("static/logo.jpg"))
    lbl_logo = ttk.Label(image=image_logo)
    lbl_logo.pack()
    btn_convert_grid = ttk.Button(text="Import Grid To Solve",command=lambda: read_gin(window))
    btn_convert_grid.pack()
    lbl_menu = ttk.Label(text="Created by TAHA Anthony, HAJJ ASSAF Sam, FAWAZ Jad, EL CHAMAA Mohammad.")
    lbl_menu.pack()
    window.mainloop()

if __name__ == "__main__":  
    menu()