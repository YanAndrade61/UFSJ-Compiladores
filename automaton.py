class Automaton:
    def __init__(self, config: dict):
        self.type = config['type']
        self.start = config['start']
        self.ends = set(config['ends'])
        self.rules = config['rules']
    
    def process(self, string: str):
        
        states_on = set([self.start])
        states_on |= self.next_state(self.start,"vz")
                
        for symbol in string:

            #Update the active states
            states = set()
            for s in states_on:
                states |= self.next_state(s,symbol)
                states |= self.next_state(s,"vz")
                               
            states_on = states

        return len(states_on & self.ends) > 0
    
    def process_stack(self, string: str):
        stacks_old = {("vz",): [self.start]}
        self.void_rule(state=self.start, stack=("vz",), stacks_now=stacks_old)
                
        for symbol in string:
            stacks_now = {}
            # print("Letra:", symbol)

            for stack, states in stacks_old.items():
                # print("\tPilha:", stack)
                for state in states:
                    # print("\tEstado:", state)
                    self.next_state_stack(state=state, symbol=symbol, stack=stack, stacks_now=stacks_now)
                    
            stacks_old = stacks_now
            # print(stacks_old)

        # print("acabou a palavra")
        
        for stack, states in stacks_old.items():
            for state in states:
                if stack[-1] == 'vz' and state in self.ends:
                    return 1
                if self.end_state(state=state, stack=stack) > 0:
                    return 1
        
        return 0
        
    def process_step_by_step(self, string: str):
        
        states_on = set([self.start])
        states_on |= self.next_state(self.start,"vz")

        all_states = []
        all_states.append(states_on)

        for symbol in string:

            #Update the active states
            states = set()
            for s in states_on:
                states |= self.next_state(s,symbol)
                               
            states_on = states
            all_states.append(states_on)

        return len(states_on & self.ends) > 0, all_states
    
    def process_step_by_step_stack(self, string: str):
        stacks_old = {("vz",): [self.start]}
        self.void_rule(state=self.start, stack=("vz",), stacks_now=stacks_old)

        states_on = set([state for stack, states in stacks_old.items() for state in states])
        all_states = []
        all_states.append(states_on)
                
        for symbol in string:
            stacks_now = {}
            # print("Letra:", symbol)

            for stack, states in stacks_old.items():
                # print("\tPilha:", stack)
                for state in states:
                    # print("\tEstado:", state)
                    self.next_state_stack(state=state, symbol=symbol, stack=stack, stacks_now=stacks_now)
                    
            stacks_old = stacks_now
            states_on = set([state for stack, states in stacks_old.items() for state in states])
            all_states.append(states_on)
            # print(stacks_old)

        # print("acabou a palavra")
        
        for stack, states in stacks_old.items():
            for state in states:
                if stack[-1] == 'vz' and state in self.ends:
                    return 1, all_states
                if self.end_state(state=state, stack=stack) > 0:
                    states_on = set(self.ends)
                    all_states.append(states_on)
                    return 1, all_states
        
        return 0, all_states
        

    def next_state(self,state: str, symbol: str):
        return set(self.rules[state].get(symbol,[]))
    
    def next_state_stack(self,state: str, symbol: str, stack: tuple, stacks_now: dict):
        states_rules = self.rules.get(state, {})
        for rule in states_rules:
            # print("regras: ",rule)
            if rule[0] != symbol: continue
            if stack[-1] != rule[1] and rule[1] != 'vz' and rule[1] != '?': continue
            if rule[1] == '?' and stack[-1] != 'vz': continue
            
            if (rule[1] == 'vz') or (rule[1] == '?'):
                stack_nex = list(stack)
            else:
                stack_nex = list(stack[:-1])
            if len(stack_nex) == 0: stack_nex.append("vz")
            if(rule[2] != "vz"):
                stack_nex = stack_nex + [c for c in rule[2]]
            
            for state_nex in rule[3]:
                stacks_now.setdefault(tuple(stack_nex), []).append(state_nex)
                self.void_rule(state=state_nex, stack=tuple(stack_nex), stacks_now=stacks_now)

    def end_state(self,state: str, stack: str):
        states_rules = self.rules.get(state, {})
        for rule in states_rules:

            if rule[0] != '?' or stack[-1] != "vz": continue
            
            for state_on in rule[3]:
                if state_on in self.ends: 
                    return 1
        
        return 0

    def void_rule(self,state: str, stack: tuple, stacks_now: dict):
        # stacks_now.setdefault(tuple(stack_nex), []).append(state_nex)
        states_rules = self.rules.get(state, {})

        for rule in states_rules:
            if rule[0] != 'vz': continue
            
            for state_nex in rule[3]:
                stacks_now.setdefault(stack, []).append(state_nex)
                self.void_rule(state=state_nex, stack=stack, stacks_now=stacks_now)

        # print("", end="")