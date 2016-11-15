what_to_execute1 = {
    "instructions": [("LOAD_VALUE", 0),
                      ("LOAD_VALUE", 1),
                      ("ADD_TWO_VALUES", None),
                      ("PRINT_ANSWER", None)],
    "numbers": [7, 5]}

what_to_execute2 = {
    "instructions": [("LOAD_VALUE", 0),
                     ("LOAD_VALUE", 1),
                     ("ADD_TWO_VALUES", None),
                     ("LOAD_VALUE", 2),
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_ANSWER", None)],
    "numbers": [7, 5, 8]}

class Interpreter:
    def __init__(self):
        self.stack = []
        
    def LOAD_VALUE(self, number):
        self.stack.append(number)
        
    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print answer
        
    def ADD_TWO_VALUES(self):
        first_num = self.stack.pop()
        seconde_num = self.stack.pop()
        total = first_num + seconde_num
        self.stack.append(total)
        
    def run_code(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        numbers = what_to_execute["numbers"]
        for each_step in instructions:
            instruction, argument = each_step
            if instruction == "LOAD_VALUE":
                self.LOAD_VALUE(numbers[argument])
            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VALUES()
            elif instruction == "PRINT_ANSWER":
                self.PRINT_ANSWER()

interpreter = Interpreter()
interpreter.run_code(what_to_execute1)
interpreter.run_code(what_to_execute2)                