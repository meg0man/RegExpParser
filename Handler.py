from NDFSA import State, NFA

class Handler:
    def __init__(self):
        self.handlers = {'CHAR' : self.handle_char,
                         'CONCAT' : self.handle_concat,
                         'ALT' : self.handle_alt,
                         'STAR' : self.handle_star
                         }
        self.state_count = 0

    def create_state(self):
        new_state = State('q' + str(self.state_count))
        self.state_count += 1
        return new_state

    def handle_char(self, t, nfa_stack):
        q0 = self.create_state()
        q1 = self.create_state()
        q0.transitions[t.value] = q1
        nfa = NFA(q0, q1)
        nfa_stack.append(nfa)

    def handle_concat(self, t, nfa_stack):
        p1 = nfa_stack.pop()
        p0 = nfa_stack.pop()

        p0.end.transitions.update(p1.start.transitions)
        p0.end.epsilon_moves.extend(p1.start.epsilon_moves)
        p0.end.is_end = False
        p1.start.dispose()

        nfa = NFA(p0.start, p1.end)
        nfa_stack.append(nfa)


    def handle_alt(self, t, nfa_stack):
        p1 = nfa_stack.pop()
        p0 = nfa_stack.pop()

        # initial alternation state
        q0 = self.create_state()

        # create epsilon moves from init state to alt states
        q0.epsilon_moves = [p0.start, p1.start]

        # create exiting alt state
        q1 = self.create_state()

        # create epsilon moves from alt states to exit
        p0.end.epsilon_moves.append(q1)
        p1.end.epsilon_moves.append(q1)
        p0.end.is_end = False
        p1.end.is_end = False
        nfa = NFA(q0, q1)
        nfa_stack.append(nfa)


    def handle_star(self, t, nfa_stack):
        p0 = nfa_stack.pop()
        q0 = self.create_state()
        q1 = self.create_state()
        q0.epsilon_moves = [p0.start]
        q0.epsilon_moves.append(q1)
        p0.end.epsilon_moves.extend([q1, p0.start])
        p0.end.is_end = False
        nfa = NFA(q0, q1)
        nfa_stack.append(nfa)