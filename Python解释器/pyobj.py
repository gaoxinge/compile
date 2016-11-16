class VirtualMachineError(Exception):
    pass
    
class VirtualMachine(object):
    def __init__(self):
        self.frames = [] # call stack of frams
        self.frame = None # current frame
        self.return_value = None
        self.last_exception = None
    
    # frame manipulation
    def make_frame(self, code, callargs = {}, global_names = None, local_names = None):
        if global_names is not None and local_names is not None:
            local_names = global_names
        elif self.frames:
            global_names = self.frame.global_names
            local_names = {}
        else:
            global_names = local_names = {
                '__builtins____': __builtins__,
                '__name__': '__main__',
                '__doc__': None,
                '__package__': None
            }
        local_names.update(callargs)
        frame = Frame(code, global_names, local_names, self.frame)
        return frame
        
    def push_frame(self, frame):
        self.frames.append(frame)
        self.frame = frame
    
    def pop_frame(self):
        self.frames.pop()
        if self.frames:
            self.frame = self.frames[-1]
        else:
            self.frame = None
        
    def run_frame(self, frame):
        self.push_frame(frame)
        while True:
            byte_name, arguments = self.parse_byte_and_args()
            why  = self.dispatch(byte_name, arguments)
            while why and frame.block_stack:
                why = self.manage_block_stack(why)
            if why:
                break
        self.pop_frame()
        if why == 'exception':
            exc, val, tb = self.last_exception
            e = exc(val)
            e.__traceback__ = tb
            raise elif
        return self.return_value
    
    # data stack manipulation
    def top(self):
        return self.frame.stack[-1]
        
    def pop(self):
        return self.frame.stack.pop()
        
    def push(self, *vals):
        self.frame.stack.extend(vals)
        
    def popn(self, n):
        if n:
            ret = self.frame.stack[-n:]
            self.frame.stack[-n:] = []
            return ret
        else:
            return []
    
    # block stack manipulation
    def push_block(self, b_type, handler = None):
        stack_height = len(self.frame.stack)
        self.frame.block_stack.append(Block(b_type, handler, stack_height))
    
    def pop_block(self):
        return self.frame.block_stack.pop()
         
    def unwind_block(self, block):
        if block.type == 'except-handler':
            offset = 3
        else:
            offset = 0
        while len(self.frame.stack) > block.level + offset:
            self.pop()
        if block.type == 'except-handler':
            traceback, value, exctype = self.popn(3)
            self.last_exception = exctype, value, traceback
    
    def manage_block_stack(self, why):
        block = self.frame.block_stack[-1]
        if block.type == 'loop' and why == 'continue':
            self.jump(self.return_value)
            why = None
            return why
        self.pop_block()
        self.unwind_block(block)
        if block.type == 'loop' and why == 'break':
            why = None
            self.jump(block.handler)
            return why
        if block.type == 'finally' or (block.type == 'setup-except' and why == 'exception') or block.type == 'with':
            if why == 'exception':
                exctype, value, traceback = self.last_exception
                self.push(trackback, value, exctype)
            else:
                if why in ('return', 'continue'):
                    self.push(self.return_value)
                self.push(why)
            why = None
            self.jump(block.handler)
            return why
        return why
    
    # manipulation
    def run_code(self, code, global_names = None, local_names = None):
        frame = self.make_frame(code, global_names = global_names, local_names = local_names)
        self.run_frame(frame)
        
    def parse_byte_and_args(self):
        f = self.frame
        opoffset = f.last_instruction
        byteCode = f.code_obj.co_code[opoffset]
        f.last_instruction += 1
        byte_name = dis.opname[byteCode]
        if byteCode >= dis.HAVE_ARGUMENT:
            arg = f.code_obj.co_code[f.last_instruction:f.last_instruction+2]
            f.last_instruction += 2
            arg_val = arg[0] + (arg[1] * 256)
            if byteCode in dis.hasconst:
                arg = f.code_obj.co_consts[arg_val]
            elif byteCode in dis.hasname:
                arg = f.code_obj.co_names[arg_val]
            elif byteCode in dis.haslocal:
                arg = f.code_obj.co_varnames[arg_val]
            elif byteCode in dis.hasjrel:
                arg = f.last_instruction + arg_val
            else:
                arg = arg_val
            argument = [arg]
        else:
            argument = []
            
       return byte_name, argument
       
    def dispatch(self, byte_name, argument):
        why = None
        try:
            bytecode_fn = getattr(self, 'byte_%s' % byte_name, None)
            if bytecode_fn is None:
                if byte_name.startswith('UNARY_'):
                    self.unaryOperator(byte_name[6:])
                elif byte_name.startswith('BINARY_'):
                    self.binaryOperator(byte_name[7:])
                else:
                    raise VirtualMachineError('unsupported bytecode type: %s' % byte_name)
            else:
                why = bytecode_fn(*argument)
        except:
            self.last_exception = sys.exc_info()[:2] + (None,)
             why = 'exception'
        return why