class EventSourcer():
    # Do not change the signature of any functions

    def __init__(self):
        self.value = 0
        self.historical_val = []
        # two stacks to keep track of undo/redos
        self.undo_ = []
        self.redo_ = []

    def add(self, num: int):
        self.historical_val.append(("Add", num, self.value))
        self.undo_.append(num)
        self.value += num

    def subtract(self, num: int):
        self.historical_val.append(("Subtract", num, self.value))
        self.undo_.append(num * -1)
        self.value -= num

    def undo(self):
        if self.undo_:
            operation = self.undo_.pop()
            if operation >= 0:
                self.historical_val.append(("Undo add", operation, self.value))
            else:
                self.historical_val.append(("Undo subtract", operation, self.value))
            self.redo_.append(operation)
            # we use -= as we are technically undoing the operation
            self.value -= operation

    def redo(self):
        if self.redo_:
            operation = self.redo_.pop()
            if operation >= 0:
                self.historical_val.append(("Redo add", operation, self.value))
            else:
                self.historical_val.append(("Redo subtract", operation, self.value))
            self.value += operation
            self.undo_.append(operation)

    def bulk_undo(self, steps: int):
        for i in range(steps):
            self.undo()

    def bulk_redo(self, steps: int):
        for i in range(steps):
            self.redo()

    # function for debugging/printing out historical changes
    def print_history(self):
        for operation in self.historical_val:
            if "add" in operation[0]:
                connector = "to"
            else:
                connector = "from"
            
            print(operation[0], operation[1], connector, operation[2])
        
        print("Current/Final value is", self.value)