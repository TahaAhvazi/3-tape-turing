import tkinter as tk

class TuringMachine:
    def __init__(self, states, tapes, transitions, initial_state, accept_state, reject_state, blank_symbol='<>'):
        self.states = states
        self.tapes = [list(tape) for tape in tapes]
        self.transitions = transitions
        self.current_state = initial_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol
        self.head_positions = [0, 0, 0]
        self.transition_history = []

    def step(self):
        read_symbols = []
        for i in range(3):
            if self.head_positions[i] < 0:
                self.tapes[i].insert(0, self.blank_symbol)
                self.head_positions[i] = 0
            elif self.head_positions[i] >= len(self.tapes[i]):
                self.tapes[i].append(self.blank_symbol)
            read_symbols.append(self.tapes[i][self.head_positions[i]])

        key = (self.current_state, tuple(read_symbols))
        print(key)  # For debugging
        if key in self.transitions:
            new_state, write_symbols, directions = self.transitions[key]
            for i in range(3):
                if write_symbols[i] != '<>':
                    self.tapes[i][self.head_positions[i]] = write_symbols[i]
                if directions[i] == 'L':
                    self.head_positions[i] -= 1
                elif directions[i] == 'R':
                    self.head_positions[i] += 1
            self.current_state = new_state
            self.transition_history.append((self.current_state, [tape[:] for tape in self.tapes]))  # Record transition history
        else:
            self.current_state = self.reject_state

    def execute(self):
        while self.current_state != self.accept_state and self.current_state != self.reject_state:
            self.step()
            self.transition_history.append((self.current_state, [tape[:] for tape in self.tapes]))  # Record transition history

        return self.current_state == self.accept_state

    def add_transition(self, current_state, read_symbols, new_state, write_symbols, directions):
        self.transitions[(current_state, tuple(read_symbols))] = (new_state, write_symbols, directions)

def load_transitions():
    states = {'q0', 'q1', 'qa', 'qr'}
    transitions = {
        ('q0', ('a', 'b', 'c')): ('q1', ('X', 'Y', 'Z'), ('R', 'R', 'R')),
        ('q1', ('a', 'b', 'c')): ('q1', ('X', 'Y', 'Z'), ('R', 'R', 'R')),
        ('q1', ('<>', '<>', '<>')): ('qa', ('<>', '<>', '<>'), ('L', 'L', 'L')),
    }
    accept_state = 'qa'
    reject_state = 'qr'
    return states, transitions, accept_state, reject_state

class TuringMachineApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Three-Tape Turing Machine")

        self.states, self.transitions, self.accept_state, self.reject_state = load_transitions()
        self.initial_state = 'q0'
        self.blank_symbol = '<>'

        self.tapes = ['', '', '']
        self.tm = TuringMachine(self.states, self.tapes, self.transitions, self.initial_state, self.accept_state, self.reject_state, self.blank_symbol)

        self.create_widgets()
        self.create_history_display()
    
    def create_widgets(self):
        self.tape_labels = []
        self.head_labels = []

        for i in range(3):
            frame = tk.Frame(self)
            frame.pack(pady=5)

            tape_frame = tk.Frame(frame)
            tape_frame.pack(side='top')
            tape_labels_row = []
            for _ in range(20):  # Assuming max tape length to display
                label = tk.Label(tape_frame, text=' ', font=('Courier', 24))
                label.pack(side='left')
                tape_labels_row.append(label)
            self.tape_labels.append(tape_labels_row)

            head_frame = tk.Frame(frame)
            head_frame.pack(side='top')
            head_labels_row = []
            for _ in range(20):  # Assuming max tape length to display
                label = tk.Label(head_frame, text=' ', font=('Courier', 24))
                label.pack(side='left')
                head_labels_row.append(label)
            self.head_labels.append(head_labels_row)

        self.input_label = tk.Label(self, text="Input String:", font=('Arial', 14))
        self.input_label.pack(pady=10)

        self.input_entry = tk.Entry(self, font=('Arial', 14))
        self.input_entry.pack(pady=10)

        self.run_button = tk.Button(self, text="Run", font=('Arial', 14), command=self.run_machine)
        self.run_button.pack(pady=10)

        self.step_button = tk.Button(self, text="Step-by-Step", font=('Arial', 14), command=self.run_machine_stepwise)
        self.step_button.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=('Arial', 14))
        self.result_label.pack(pady=10)

    def create_history_display(self):
        self.history_label = tk.Label(self, text="Transition History:", font=('Arial', 14))
        self.history_label.pack(pady=10)

        self.text_history = tk.Text(self, height=10, width=60, font=('Courier', 12))
        self.text_history.pack(pady=10)

    def update_history_display(self):
        self.text_history.config(state=tk.NORMAL)
        self.text_history.delete('1.0', tk.END)
        self.text_history.insert(tk.END, "Transition History:\n")
        for transition in self.tm.transition_history:
            self.text_history.insert(tk.END, f"{transition}\n")
        self.text_history.config(state=tk.DISABLED)

    def run_machine(self):
        input_string = self.input_entry.get()
        
        # Compute segment length
        segment_length = len(input_string) // 3
        
        # Distribute the input string into three tapes
        self.tm.tapes = [
            list(input_string[:segment_length]),   # First tape gets first segment
            list(input_string[segment_length:2*segment_length]),   # Second tape gets second segment
            list(input_string[2*segment_length:]),   # Third tape gets third segment
        ]
        
        if self.tm.execute():
            self.result_label.config(text="The string is valid according to the Turing Machine's rules.", fg='green')
        else:
            self.result_label.config(text="The string is not valid according to the Turing Machine's rules.", fg='red')

        self.update_display()
        self.update_history_display()

    def run_machine_stepwise(self):
        input_string = self.input_entry.get()
        
        # Compute segment length
        segment_length = len(input_string) // 3
        
        # Distribute the input string into three tapes
        self.tm.tapes = [
            list(input_string[:segment_length]),   # First tape gets first segment
            list(input_string[segment_length:2*segment_length]),   # Second tape gets second segment
            list(input_string[2*segment_length:]),   # Third tape gets third segment
        ]
        
        self.tm.current_state = self.initial_state
        self.tm.head_positions = [0, 0, 0]
        self.tm.transition_history = []

        self.update_display()  # Show the initial state and tapes before starting
        self.after(1000, self.execute_step)

    def execute_step(self):
        if self.tm.current_state != self.accept_state and self.tm.current_state != self.reject_state:
            self.tm.step()
            self.update_display()
            self.update_history_display()
            self.after(1000, self.execute_step)  # Schedule next step in 1000 ms (1 second)
        else:
            if self.tm.current_state == self.accept_state:
                self.result_label.config(text="The string is valid according to the Turing Machine's rules.", fg='green')
            else:
                self.result_label.config(text="The string is not valid according to the Turing Machine's rules.", fg='red')

    def update_display(self):
        for i in range(3):
            for j in range(20):  # Clear previous labels
                self.tape_labels[i][j].config(text=' ')
                self.head_labels[i][j].config(text=' ')
            for j, char in enumerate(self.tm.tapes[i]):
                self.tape_labels[i][j].config(text=char)
            self.head_labels[i][self.tm.head_positions[i]].config(text='^')

if __name__ == "__main__":
    app = TuringMachineApp()
    app.mainloop()
