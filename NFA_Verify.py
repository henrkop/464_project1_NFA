"""
Full NFA Verifier Implementation
Implemented by Gabriel Kaim, Henry Kopp, and Colin Ruark
"""

#opening the file
with open('nfa.txt', 'r') as nfa_file:
    #initializing each separate line for computation and input string
    lines = nfa_file.read().splitlines()
    s = ''

    #breaking up the lines by important info
    numStates = int(lines[0])
    startState = lines[1]
    numAccepts = int(lines[2])
    accepts = list()

    for i in range(numAccepts):
        accepts.append(lines[i + 3])

    alphabet = list()
    for ch in lines[numAccepts + 3]:
        alphabet.append(ch)
    
    numTransitions = int(lines[numAccepts + 4])
    transitions = list()

    for i in range(numTransitions):
        transitions.append(lines[i + numAccepts + 5].split(','))
    
    print(str(numStates) + " states")
    print("start at " + startState)
    print(str(numAccepts) + " accept states:")
    print("- " + "\n- ".join(accepts))
    print("Alphabet: " + ", ".join(alphabet))
    print(str(numTransitions) + " transitions: ")
    print("- " + "\n- ".join(", ".join(transition) for transition in transitions))
    print("string " + (s if s else "NONE"))

    #epsilon transitions must add the new state AND keep the old state in the set of current reached states
    def epsilons(states, transitions):
        prev = set(states)
        stack = list(states)
        while len(stack) > 0:
            current = stack.pop()
            for t in transitions:
                if t[0] == current and t[1] == 'E':
                    if t[2] not in prev:
                        prev.add(t[2])
                        stack.append(t[2])
        return prev

    #Starting off by calculating epsilons from the start state
    current_states = epsilons({startState}, transitions)

    #walk the string
    for ch in s:
        next_states = set()
        
        #takes the current states and adds to the set of next states by following character transitions
        for state in current_states:
            for t in transitions:
                if t[0] == state and t[1] == ch:
                    next_states.add(t[2])

        #updates by epsilons again
        current_states = epsilons(next_states, transitions)
        
        #edge case, input character provided not in alphabet
        if ch not in alphabet:
            print("Character " + ch + " NOT IN ALPHABET")
            current_states = set()
            break

        #edge case for when no transitions lead to a new state
        if not current_states:
            print("NO REMAINING STATES")
            break
            
    
    print("Ending states: " + (", ".join(current_states) if current_states else "None"))
            
    #cross-references all reached states against all accept states
    acceptStateFound = False
    for state in current_states:
        if state in accepts:
            acceptStateFound = True
    
    #final accept/reject of string in NFA
    print("Accept NFA? " + str(acceptStateFound))