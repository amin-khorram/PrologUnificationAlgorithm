
# Writing Prolog Unification Algorithm Using Python

#enter the first and second terms
inp1 = input("Please insert the first term\n") 
inp2 = input("please insert the second term\n") 

#define a function that receives the output of analyze function and prints the unification output
def unify(inp1,inp2):
    #define an empty list of variables
    var  = [] 
    #define an empty list of temporary variables
    tempvar  = []  
    #the status of our algorithm (4 status are defined: initiate,yes,no,input error)
    status ="initiate" 
    #while the status of algorithm is initiate
    while status =="initiate":
        if len(tempvar)==0:
            #if the temporary list of variables is empty them start analyzing the algorithm using analyze function
            status = analyze(inp1,inp2,var,tempvar)            
        else:
            #if the temporary list of variables is not empty, 
            #replace the first variable of the temporary variable list with the second variable of temporary varible list in the input arguments           
            inp1=inp1.replace(tempvar[0][0], tempvar[0][1]) 
            inp2=inp2.replace(tempvar[0][0], tempvar[0][1])
            #after replacing and before continuing the analyze, empty the list of temporary variables
            tempvar =[] 
            #analyze again
            status = analyze(inp1,inp2,var,tempvar)
    #print according to the status        
    if status == "no":
        print ("no")         
        var=[]
    elif status == "input error":
        print ("input error")
        var=[]   
    elif status == "yes":
        print ("yes")
        for i in range(len(var)):
            #also print the unified arguments
            print(var[i][0] + " = " + var[i][1])

#function to detect the constant or variable type of input
def cons_var(inp):
    for i in inp:
        #if the first letter of input is lowercase it is constant, and if it is uppercase is a variable
        if i.islower():
            return "constant"
        else:
            return "variable"
        
#function to determine the type of input        
def inp_type(inp):
    #if input has these three elements may be function
    if  "(" in inp or ")" in inp or "," in inp:
        #if input has both paranthesis then it is a function
        if "(" in inp:
            if ")" in inp:
                return "function"                
            else:
                #if the input misses one of paranthesis
                return "input error"
            
    if "(" not in inp and ")" not in inp and "," not in inp:
        # if none of these three elements ")" , "(" , "," are in the inputs, call the cons_var function
        inp_type =cons_var(inp)
        return inp_type            
    else:
        # Return input error for unacceptable characters
        return "input error" 

#function to convert a given function to its elements and put them in a list   
def convlist(inp):
    convlist=[i.split('\t')[0] for i in inp]
    return convlist
    
#function to determine the name of function
def functor(inp):
    #call the convlist function
    funclist=convlist(inp)
    #take the first element of convlist function as functor
    funname=funclist[0]
    return funname

#function to substitute variables in the temporary variable list and variable list
def substitute(var,tempvar):
    for i in range(len(var)):
        #if the first element of temporary variable list in the second elements of variable list
        if tempvar[0][0] in var[i][1]:
            var[i][1]= var[i][1].replace(tempvar[0][0],tempvar[0][1])

#function to determine the number of arguments in the function
def func_ele (tempele):
    #start the list of arguments empty
    argu = [] 
    #start the argument status empty
    argstat = "" 
    #start the number of commas and paranthesis equal to zero
    pr=0 
    com=0 
    #define a temporary argument value finder empty
    tempargstat =""
    #define a variable to detect the firs observed paranthesis "("
    fpar =0 
    #loop to fill the argstat when it sees the first paranthesis "("
    for i in tempele:
        if fpar ==1: 
            argstat =argstat +i
        if i=="(":
            fpar =1
    #now remove the last element from argstat which is ")"        
    argstat = argstat[:-1]
    #loop to find the number of commas and fill the list of arguments with temporary argument values
    for j in argstat:
        if j=="," and pr==0:
            com=com+1 
            argu.append(tempargstat)
            tempargstat =""
        else:
            tempargstat = tempargstat + j
        #if see "(" increase the number of paranthesis
        if j =="(": 
            pr=pr+1 
        #if see ")" decrease the number of paranthesis
        elif j == ")":
            pr=pr-1
    #if the number of commas is o the only found argument will be appended to the list of arguments
    if com==0:
        argu.append(argstat)
    else:
        # otherwise the last argument is added to the argument list
        argu.append(tempargstat)
    return (argu)
    
#The recursive function that analyze each two inputs and drive the output which will be called by unify function
def analyze(inp1,inp2,var,tempvar):
    #the status of algorithm is initiate
    status = "initiate"
    # check the type of inputs
    inp1type = inp_type(inp1) 
    inp2type = inp_type(inp2)
    #in case both inputs are errors
    if inp1type == "input error" or inp2type == "input error": 
        return "input error"
    #in case that either one of inputs is function
    if inp1type == "function" or inp2type =="function":
        #in case that one function and one constant the result is no
        if inp1type == "constant" or inp2type == "constant": 
            return "no" 
        else:
            #in case of one function and one variable
            if inp1type =="variable" and inp2type =="function": 
                #first check if the variable is in the function
                if inp1 in inp2:
                    #it returns infinite loop
                    return "no" 
                else:
                    #first append the variables to the temporary variable list                                                      
                    tempvar.append([inp1,inp2])
                    #if the list of variables is not empty
                    if var!=[]:
                        #substitute the variables of the temporary variable list in the variable list by calling the substitute function
                        substitute(var,tempvar)
                    #append variables to the variable list
                    var.append([inp1,inp2]) 
                    #and set the status equal to initiate again to replace the variables in the temporary variable list with the inputs (in the unify function)
                    return "initiate"
            #else if input2 is variable and input 1 is function
            elif inp2type =="variable" and inp1type =="function":
                #again check if the variable is in the function
                if inp2 in inp1:
                    #if so it is an infinite loop, return no
                    return "no" 
                else:
                    #otherwise, first append the variables to the temporary variable list                                                      
                    tempvar.append([inp1,inp2])
                    #if the list of variables is not empty
                    if var!=[]:
                        #substitute the variables of the temporary variable list in the variable list by calling the substitute function
                        substitute(var,tempvar)
                    #append variables to the variable list    
                    var.append([inp1,inp2])
                    #return initiate to replace the variables in the temporary variable list with the inputs
                    return "initiate"
            #Now if both inputs are function
            else:
                #check the functor of the first input
                f1 = functor(inp1)
                #check the functor of the second input
                f2 = functor(inp2)
                #check the arity for the first input
                n1= len(func_ele(inp1))
                #check the arity for the second input
                n2 = len(func_ele(inp2))
                #if the inputs are error the result is error
                if inp1type =="input error" or inp2type =="input error": 
                    return "input error" 
                #first check if the functors and arities are the same
                if f1 ==f2 and n1==n2: 
                    #set a counter to analyze each argument of the input1 and input2 according to the current number of counter
                    counter = 0;
                    #find the arguments of input1 using the func_ele function
                    argument1 = func_ele(inp1) 
                    #find the arguments of input2 using the func_ele function
                    argument2 = func_ele(inp2)
                    #check each argument of inputs
                    while counter< n1: 
                        #start with initiate status
                        status ="initiate" 
                        #analyze the nth argument from arguments lists
                        status = analyze(argument1[counter],argument2[counter],var,tempvar)# analyze the analyze function again 
                        #if the result status is initiate, return initiate as the response of unify function
                        if status =="initiate":
                            return "initiate"
                        #if the result status is no, return no as the result of unify function
                        elif status =="no":
                            return "no"
                        #if the status is input error, return input error as the result of unify function
                        elif status =="input error":
                            return "input error"
                        #finally if the status is yes, and it is the last argument of function, return yes and increase the counter by one to sease the loop
                        elif status =="yes" and counter==(n1-1):
                            counter =counter +1
                            return "yes"
                        #if the status is yes and it is not the last argument of function, just increase the counter and remain in the loop
                        else: 
                            counter=counter+1
                #return no if the functors or arities are not equal
                else:
                    return "no" 
    # now if both inputs are constant            
    elif inp1type == "constant" and inp2type =="constant": 
        #if the inputs are exactly equal return yes
        if inp1==inp2: 
            return "yes"
        else:
            #and return no if they are not equal
            return "no"
     #if one of inputs is variables   
    elif inp1type =="variable" or inp2type =="variable": 
        #if input1 is variable
        if inp1type =="variable":
            #if input2 is variable
            if inp2type == "variable":
                #if two inputs are eual return yes
                if inp1==inp2: 
                    return "yes" 
                #if the inputs are not equal
                else:
                    #first append the variables to the temporary variable list                                                      
                    tempvar.append([inp1,inp2])
                    #if the list of variables is not empty
                    if var!=[]:
                        #substitute the variables of the temporary variable list in the variable list by calling the substitute function
                        substitute(var,tempvar)
                    #append variables to the variable list
                    var.append([inp1,inp2])
                    #again return initiate to replace the variables in the temporary variable list with the inputs
                    return "initiate" 
            #if input2 is not variable    
            else:
                #first append the variables to the temporary variable list
                tempvar.append([inp1,inp2]) 
                #if the list of variables is not empty
                if var!=[]:
                    #substitute the variables of the temporary variable list in the variable list by calling the substitute function
                    substitute(var,tempvar)
                #append variables to the variable list
                var.append([inp1,inp2])
                #again return initiate to replace the variables in the temporary variable list with the inputs (in the unify function)
                return "initiate"
        #if input1 is not variable
        else:
            #first append the variables to the temporary variable list
            tempvar.append([inp2,inp1]) 
            #if the list of variables is not empty
            if var!=[]:
                #substitute the variables of the temporary variable list in the variable list by calling the substitute function
                substitute(var,tempvar)
            #append variables to the variable list
            var.append([inp2,inp1])
            #again return initiate to replace the variables in the temporary variable list with the inputs(in the unify function)                  
            return "initiate"

#call the unify function
unify(inp1,inp2)
  
       
