class Node: 
    def __init__(self, lexem):
        self.lexem = lexem
        self.children = [] #vetor de filhos  
        self.type = None
        self.op = None
        self.value = None

    def verify_type(self):
        for child in self.children:
            child.verify_type()

    def __str__(self, level=0):
        ret = "   "*level+ repr(self) +"\n"
        if self.op != None: 
            ret += "   "*level+ self.op +"\n"
            level += 1
        for child in self.children:
            if (child != None):
                ret += child.__str__(level+1) #level+1
        return ret

class NodeExprAritmetica(Node): 
    def __init__(self, op, left, right):
        Node.__init__(self,'ExprAritmetica')
        self.children.append(left)
        self.children.append(right)
        self.op = op

    def verify_type(self):
        type1 = self.children[0].verify_type()
        type2 = self.children[1].verify_type()
        if type1 != type2:
            with open('logs/error.log','a') as fp:
                print(f'ERRO SEMANTICO TIPOS DIFERENTES: {self.children[0].lexem}({type1}) e {self.children[1].lexem}({type2})', file=fp)
            return 'Error'
        else:
            return type1

    def __repr__(self):
        return "ExprAritmetica: " 
        

class NodeId(Node):
    def __init__(self, lexem, type_):
        Node.__init__(self,lexem)
        self.type = type_

    def verify_type(self):
        return self.type

    def __repr__(self):
        return "NoId: " + str(self.lexem) 

class NodeIntConst(Node):
    def __init__(self, value, type = 'int'):
        Node.__init__(self,"NoInt")
        self.value = value
        self.type = type

    def verify_type(self):
        return self.type

    def __repr__(self):
        return "NoInt: " + str(self.value)

class NodeCharConst(Node):
    def __init__(self, value, type = 'char'):
        Node.__init__(self,"NoChar")
        self.value = value
        self.type = type
    
    def verify_type(self):
        return self.type

    def __repr__(self):
        return "NoChar: " + str(self.value)

class NodeFloatConst(Node):
    def __init__(self, value, type = 'float'):
        Node.__init__(self,"NoFloat")
        self.value = value
        self.type = type

    def verify_type(self):
        return self.type

    def __repr__(self):
        return "NoFloat: " + str(self.value)

class NodeAssign(Node):
    def __init__(self, left, right):
        Node.__init__(self,"NoAssign")
        self.children.append(left)
        self.children.append(right)

    def verify_type(self):
        type1 = self.children[0].verify_type()
        type2 = self.children[1].verify_type()
        if type1 != type2:
            with open('logs/error.log','a') as fp:
                print(f'ERRO SEMANTICO TIPOS DIFERENTES: {self.children[0].lexem}({type1}) e {self.children[1].lexem}({type2})', file=fp)

    def __repr__(self):
        return "NoAssign: "
    
class NodeIf(Node):
    def __init__(self, condition, then, else_ = None):
        Node.__init__(self,"NoIf")
        self.children.append(condition)
        self.children.append(then)
        if else_: self.children.append(else_)

    def __repr__(self):
        return "NoIf: "

class NodeWhile(Node):
    def __init__(self, condition, block):
        Node.__init__(self,"NoWhile")
        self.children.append(condition)
        self.children.append(block)
    
    def verify_type(self):
        return self.children[0].verify_type()

    def __repr__(self):
        return "NoWhile: "

class NodeBlock(Node):
    def __init__(self):
        Node.__init__(self,"NoBlock")

    def __repr__(self):
        return "NoBlock: "

class NodePrint(Node):
    def __init__(self, value, newline):
        Node.__init__(self,"NoPrint")
        self.newline = newline
        self.children.append(value)
    
    def verify_type(self):
        return self.children[0].verify_type()

    def __repr__(self):
        return "NoPrint: "

class NodeReturn(Node):
    def __init__(self, value):
        Node.__init__(self,"NoReturn")
        self.children.append(value)

    def verify_type(self):
        return self.children[0].verify_type()

    def __repr__(self):
        return "NoReturn: "
    
class NodeFunction(Node):
    def __init__(self, name):
        self.name = name
        Node.__init__(self,"NoFunction")

    def __repr__(self):
        return f"NoFunction - {self.name}: "