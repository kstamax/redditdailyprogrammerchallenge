# A binary array is an array consisting of only the values 0 and 1. 
# Given a binary array of any length, 
# return an array of positive integers that represent the lengths of the sets of consecutive 1's in the input array, 
# in order from left to right.

# Solution: Define counter = 0, loop through list, if element == 1 -> add 1 to counter, 
# else check if counter > 0, if true append counter to result array, make counter 0, go to next iteration, 
# after loop if counter > 0 -> append it one more time to result array
# return result at the end

def nonogramrow(row):
    res = [] # result list
    c = 0 # counter
    for el in row:
        if el == 1:
            c +=1
        elif el == 0:
            if c > 0:
                res.append(c)
                c = 0
        else:
            print('Invalid number in list')
            return -1
    if c > 0:
        res.append(c)        
    return res



# Tests
tests = [
    {
        'input':[],
        'output':[]
    },
    {
        'input':[0,0,0,0,0],
        'output':[]
    },
    {
        'input':[1,1,1,1,1],
        'output':[5]
    },
    {
        'input':[0,1,1,1,1,1,0,1,1,1,1],
        'output':[5,4]
    },
    {
        'input':[1,1,0,1,0,0,1,1,1,0,0],
        'output':[2,1,3]
    },
    {
        'input':[0,0,0,0,1,1,0,0,1,0,1,1,1],
        'output':[2,1,3]
    },
    {
        'input':[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        'output':[1,1,1,1,1,1,1,1]
    }
]

for test in tests:
    print('------------------------------------------------------------------')
    print('test input: ',test['input'],'\nResult: ',nonogramrow(test['input']), '\nExpected output: ',test['output'], '\nPassed: ',nonogramrow(test['input'])==test['output'], sep='')