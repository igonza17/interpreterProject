#Testing file for implementing changes
#Based on ProjectMorpheus2
#CHANGE 1.Removing Unary Operator
import string
import sys
class Index:
    def __init__(self,index,line,column):
        self.index = index
        self.line = line
        self.column = column

    def advance(self,curChar=None):
        self.index +=1
        self.column +=1
        if curChar == '\n':
            self.line+=1
            self.column+=0
        return self

    def copy(self):
        return Index(self.index,self.line,self.column)

#Tokens Implementation----------------------------------------------------------------------------------------------------
INT, FLOAT, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, IDENTIFIER, KEYWORD, EQUALS, EE, NE, LT, GT, LTE, GTE = 'INT', 'FLOAT', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'EOF', 'IDENTIFIER', 'KEYWORD', 'EQUALS', 'EE', 'NE', 'LT', 'GT', 'LTE', 'GTE'
KEYWORD=['var','if','then','elif','else', 'and', 'or', 'not']
DIGIT = '0123456789'
LETTERS = string.ascii_letters
lettersDigits = LETTERS + DIGIT

class Tokens:
    def __init__(self,type,value=None, posStart=None, posEnd=None ):
        self.type = type
        self.value = value
        if posStart:
            self.posStart = posStart.copy()
            self.posEnd = posStart.copy()
            self.posEnd.advance()
        if posEnd:
            self.posEnd = posEnd.copy()

    def matches(self,type, value ):
        return self.type == type and self.value == value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

#Lexer Implementation----------------------------------------------------------------------------------------------------
class lexer:
    def __init__(self,text):
        self.text = text
        self.pos = Index(-1,0,-1)
        self.currentToken = None
        self.advance()

    def advance(self):
        self.pos.advance(self.currentToken)
        self.currentToken = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def makeTokens(self): #Detects the type of token the data type is, and makes that specific token type
        tokensList = []
        while self.currentToken != None:
            if self .currentToken in ' \t':
                self.advance()
            elif self.currentToken in DIGIT:
                tokensList.append(self.makeNum())
            elif self.currentToken in LETTERS:
                tokensList.append(self.makeIdentifier())
            elif self.currentToken == '+':
                tokensList.append(Tokens(PLUS, posStart=self.pos))
                self.advance()
            elif self.currentToken == '-':
                tokensList.append(Tokens(MINUS,posStart=self.pos))
                self.advance()
            elif self.currentToken == '*':
                tokensList.append(Tokens(MUL,posStart=self.pos))
                self.advance()
            elif self.currentToken == '/':
                tokensList.append(Tokens(DIV,posStart=self.pos))
                self.advance()
            elif self.currentToken == '(':
                tokensList.append(Tokens(LPAREN,posStart=self.pos))
                self.advance()
            elif self.currentToken == ')':
                tokensList.append(Tokens(RPAREN,posStart=self.pos))
                self.advance()
            elif self.currentToken == '!':
                tok, error = self.makeNotEqual()
                if error:return [], error
                tokensList.append(tok)
            elif self.currentToken == '=':
                tokensList.append(self.makeEquals())
            elif self.currentToken == '<':
                tokensList.append(self.makeLessThan())
            elif self.currentToken == '>':
                tokensList.append(self.makeGreaterThan())
            else:
                # posStart = self.pos.copy()
                char = self.currentToken
                self.advance()
                return [], sys.exit("Illegal Character: " + "'" + char + "'")
        tokensList.append(Tokens(EOF, posStart=self.pos))
        return tokensList, None

    def makeNum(self): #Helps with the detection if the value is a int or float based on if there is a decimal on the token
        numStr = ''
        decimalCount = 0
        posStart = self.pos.copy()
        while self.currentToken != None and self.currentToken in DIGIT + '.':
            if self.currentToken == '.':
                if decimalCount == 1: break
                decimalCount += 1
                numStr += '.'
            else:
                numStr += self.currentToken
            self.advance()
        if decimalCount == 0:
            return Tokens(INT, int(numStr), posStart, self.pos)
        else:
            return Tokens(FLOAT, float(numStr), posStart, self.pos)

    def makeIdentifier(self):
        identifierStr = ''
        posStart = self.pos.copy()
        while self.currentToken != None and self.currentToken in lettersDigits + '_':
            identifierStr += self.currentToken
            self.advance()
        tokenType = KEYWORD if identifierStr in KEYWORD else IDENTIFIER
        return Tokens(tokenType, identifierStr,posStart,self.pos)

    def makeNotEqual(self):
        posStart = self.pos.copy()
        self.advance()
        if self.currentToken == '=':
            self.advance()
            return Tokens(NE,posStart=posStart, posEnd = self.pos),None
        self.advance()
        sys.exit("'=' goes after '!' ")

    def makeEquals(self):
        tokType = EQUALS
        posStart = self.pos.copy()
        self.advance()
        if self.currentToken == '=':
            self.advance()
            tokType = EE
        return Tokens(tokType,posStart=posStart,posEnd=self.pos)

    def makeLessThan(self):
        tokType = LT
        posStart = self.pos.copy()
        self.advance()
        if self.currentToken == '=':
            self.advance()
            tokType = LTE
        return Tokens(tokType,posStart=posStart,posEnd=self.pos)

    def makeGreaterThan(self):
        tokType = GT
        posStart = self.pos.copy()
        self.advance()
        if self.currentToken == '=':
            self.advance()
            tokType = GTE
        return Tokens(tokType, posStart=posStart, posEnd=self.pos)

#Parser Implementation--------------------------------------------------------------------------------------
class numNode:
    def __init__(self,tok):
        self.tok = tok
        self.posStart = self.tok.posStart
        self.posEnd = self.tok.posEnd

    def __repr__(self):
        return f'{self.tok}'

class varAccessNode:
    def __init__(self,varNameTok):
        self.varNameTok = varNameTok
        self.posStart = self.varNameTok.posStart
        self.posEnd = self.varNameTok.posEnd

class variableAssignNode:
    def __init__(self,varNameTok,valueNode):
        self.varNameTok = varNameTok
        self.valueNode = valueNode
        self.posStart = self.varNameTok.posStart
        self.posEnd = self.valueNode.posEnd

class operationNode:
    def __init__(self,left,opToken,right):
        self.left = left
        self.opToken = opToken
        self.right = right
        self.posStart = self.left.posStart
        self.posEnd = self.right.posEnd

    def __repr__(self):
        return f'({self.left},{self.opToken},{self.right})'

class ifNode:
    def __init__(self,case, elseCase):
        self.case = case
        self.elseCase = elseCase
        self.posStart = self.case[0][0].posStart
        self.posEnd = (self.elseCase or self.case[len(self.case)-1][0]).posEnd

class parserResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advanceCount = 0

    def resgisterAdvance(self):
        self.advanceCount += 1

    def register(self,result):
        self.advanceCount += result.advanceCount
        if result.error: self.error = result.error
        return result.node

    def success(self,node):
        self.node = node
        return self

    def failure(self,error):
        if not self.error or self.advanceCount==0:
            self.error = error
        return self

class parser: #This parser class main job is to specify the grammar of a factor,term,expression,if expression,variable expression
    def __init__(self,tokens):
        self.tokens = tokens
        self.tokensIndex = -1
        self.advance()

    def advance(self):
        self.tokensIndex += 1
        if self.tokensIndex < len(self.tokens):
            self.currentToken = self.tokens[self.tokensIndex]
        return self.currentToken

    def parse(self):
        result = self.expr()
        if not result.error and self.currentToken.type != EOF:
            sys.exit("Missing or Expected +,-,*,/,==,!=,<,>,<=,>=,and,or operators ")
        return result

#1. Control flow elements (like if statements)
    def ifExpr(self):
        res = parserResult()
        case = []
        elseCase = None
        if not self.currentToken.matches(KEYWORD,'if'):
            sys.exit("Missing or Expected KEYWORD 'if' ")
        res.resgisterAdvance()
        self.advance()
        condition = res.register(self.expr())
        if res.error:return res
        if not self.currentToken.matches(KEYWORD,'then'):
            sys.exit("Missing or Expected KEYWORD 'then' ")
        res.resgisterAdvance()
        self.advance()
        expr = res.register(self.expr())
        if res.error:return res
        case.append((condition,expr))
        while self.currentToken.matches(KEYWORD,'elif'):
            res.resgisterAdvance()
            self.advance()
            condition = res.register(self.expr())
            if res.error:return res
            if not self.currentToken.matches(KEYWORD,'then'):
                sys.exit("Missing or Expected KEYWORD 'then' ")
            res.resgisterAdvance()
            self.advance()
            expr=res.register(self.expr())
            if res.error:return res
            case.append((condition,expr))
        if self.currentToken.matches(KEYWORD,'else'):
            res.resgisterAdvance()
            self.advance()
            elseCase = res.register(self.expr())
            if res.error:return res
        return res.success(ifNode(case,elseCase))

    def variableExpr(self):
        res = parserResult()
        tok = self.currentToken
        if tok.type in (INT,FLOAT):
            res.resgisterAdvance()
            self.advance()
            return res.success(numNode(tok))
        elif tok.type == IDENTIFIER:
            res.resgisterAdvance()
            self.advance()
            return res.success(varAccessNode(tok))
        elif tok.type == LPAREN:
            res.resgisterAdvance()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.currentToken.type == RPAREN:
                res.resgisterAdvance()
                self.advance()
                return res.success(expr)
            else:
                sys.exit("Missing or Expected ')' ")
        elif tok.matches(KEYWORD,'if'):
            ifExpr = res.register(self.ifExpr())
            if res.error:return res
            return res.success(ifExpr)
        sys.exit("Missing or Expected identifier, int, float")

    def factor(self):
        result = parserResult()
        tok = self.currentToken
        if tok.type in (PLUS, MINUS):
            result.resgisterAdvance()
            self.advance()
            # factor = result.register(self.factor())
            if result.error:
                return result
            sys.exit("Unary operators are not supported")
        return self.variableExpr()

    def term(self):
        return self.operation(self.factor,(MUL,DIV))

    def arithmethicExpr(self):
        return self.operation(self.term,(PLUS,MINUS))

    def comparisonExpr(self):
        res = parserResult()
        if self.currentToken.matches(KEYWORD,'not'):
            # opToken = self.currentToken
            res.resgisterAdvance()
            self.advance()
            # node = res.register(self.comparisonExpr())
            if res.error: return res
            sys.exit("Unary operators are not supported")

        node = res.register(self.operation(self.arithmethicExpr, (EE,NE,LT,GT,LTE,GTE)))
        if res.error:
            sys.exit("Missing or Expected identifier, int, float,identifier, +, -, or '(' , 'not'")
        return res.success(node)

    def expr(self):
        res = parserResult()
        if self.currentToken.matches(KEYWORD,'var'):
            res.resgisterAdvance()
            self.advance()
            if self.currentToken.type != IDENTIFIER:
                sys.exit("Missing or Expected Identifier")
            variableName = self.currentToken
            res.resgisterAdvance()
            self.advance()
            if self.currentToken.type != EQUALS:
                sys.exit("Missing or Expected '=' ")
            res.resgisterAdvance()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(variableAssignNode(variableName,expr))
        node = res.register(self.operation(self.comparisonExpr,((KEYWORD, "and"),(KEYWORD,"or"))))
        if res.error:
            sys.exit("Missing or Expected 'var','int','float','identifier','+','-' ,'(' ")
        return res.success(node)

    def operation(self,func,op):
        res = parserResult()
        left = res.register(func())
        if res.error:
            return res
        while self.currentToken.type in op or (self.currentToken.type, self.currentToken.value) in op:
            opToken = self.currentToken
            res.resgisterAdvance()
            self.advance()
            right = res.register(func())
            if res.error:
                return res
            left = operationNode(left, opToken, right)
        return res.success(left)

#Evaluator/Interpreter-----------------------------------------------------------------------
class runtimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self,res):
        if res.error: self.error = res.error
        return res.value

    def success(self,value):
        self.value = value
        return self

    def failure(self, error):
        self.error=error
        return self

class Number:
    def __init__(self,value):
        self.value = value
        self.setPosition()
        self.setContext()

    def setPosition(self, posStart=None, posEnd=None):
        self.posStart=posStart
        self.posEnd = posEnd
        return self

    def setContext(self,context=None):
        self.context = context
        return self

    def addition(self,other):
        if isinstance(other,Number):
            return Number(self.value + other.value).setContext(self.context), None

    def subtraction(self,other):
        if isinstance(other,Number):
            return Number(self.value - other.value).setContext(self.context), None

    def multiplication(self,other):
        if isinstance(other,Number):
            return Number(self.value * other.value).setContext(self.context), None

    def division(self,other):
        if isinstance(other,Number):
            if other.value == 0:
                sys.exit('Division by zero is a Runtime Error')
            return Number(self.value / other.value).setContext(self.context), None

    def getComparisonEqual(self,other):
        if isinstance(other,Number):
            return Number(int(self.value == other.value)).setContext(self.context), None

    def getComparisonNotEqual(self,other):
        if isinstance(other,Number):
            return Number(int(self.value != other.value)).setContext(self.context), None

    def getComparisonLessThan(self,other):
        if isinstance(other,Number):
            return Number(int(self.value < other.value)).setContext(self.context), None

    def getComparisonGreaterThan(self,other):
        if isinstance(other,Number):
            return Number(int(self.value > other.value)).setContext(self.context), None

    def getComparisonLessThanEqual(self,other):
        if isinstance(other,Number):
            return Number(int(self.value <= other.value)).setContext(self.context), None

    def getComparisonGreaterThanEqual(self,other):
        if isinstance(other,Number):
            return Number(int(self.value >= other.value)).setContext(self.context), None

    def andBy(self,other):
        if isinstance(other,Number):
            return Number(int(self.value and other.value)).setContext(self.context), None

    def orBy(self,other):
        if isinstance(other,Number):
            return Number(int(self.value or other.value)).setContext(self.context), None

    def notBy(self):
        return Number(1 if self.value == 0 else 0).setContext(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.setPosition(self.posStart,self.posEnd)
        copy.setContext(self.context)
        return copy

    def isTrue(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)

class traceBackHandling:
    def __init__(self,displayName,parent = None, parentEntryPos=None ):
        self.displayName = displayName
        self.parent = parent
        self.parentEntryPos = parentEntryPos
        self.symbolTable = None

class symbolTable:
    def __init__(self):
        self.symbol = {}
        self.parent = None

    def get(self,name):
        value = self.symbol.get(name,None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self,name,value):
        self.symbol[name]=value

    def remove(self,name):
        del self.symbol[name]

class eval:
    def visit(self,node,context):
        functionName = f'visit_{type(node).__name__}'
        function = getattr(self, functionName,self.unknownFunction)
        return function(node,context)

    def unknownFunction(self,node,context):
        raise Exception(f'No visit {type(node).__name__} function determined')

    def visit_numNode(self,node,context):
        return runtimeResult().success(Number(node.tok.value).setContext(context).setPosition(node.posStart, node.posEnd))

    def visit_varAccessNode(self,node,context):
        res = runtimeResult()
        varName = node.varNameTok.value
        value = context.symbolTable.get(varName)
        if not value:
            sys.exit(varName + ' is not defined')
        return res.success(value)

    def visit_variableAssignNode(self,node,context):
        res = runtimeResult()
        varName = node.varNameTok.value
        value = res.register(self.visit(node.valueNode,context))
        if res.error:
            return res
        context.symbolTable.set(varName,value)
        return res.success(value)

    def visit_operationNode(self,node,context):
        res = runtimeResult()
        left = res.register(self.visit(node.left,context))
        if res.error:return res
        right = res.register(self.visit(node.right,context))
        if res.error:return res
        if node.opToken.type == PLUS:
            result, error = left.addition(right)
        elif node.opToken.type == MINUS:
            result, error = left.subtraction(right)
        elif node.opToken.type == MUL:
            result, error = left.multiplication(right)
        elif node.opToken.type == DIV:
            result, error = left.division(right)
        elif node.opToken.type == EE:
            result, error = left.getComparisonEqual(right)
        elif node.opToken.type == NE:
            result, error = left.getComparisonNotEqual(right)
        elif node.opToken.type == LT:
            result, error = left.getComparisonLessThan(right)
        elif node.opToken.type == GT:
            result, error = left.getComparisonGreaterThan(right)
        elif node.opToken.type == LTE:
            result, error = left.getComparisonLessThanEqual(right)
        elif node.opToken.type == GTE:
            result, error = left.getComparisonGreaterThanEqual(right)
        elif node.opToken.matches(KEYWORD,'and'):
            result, error = left.andBy(right)
        elif node.opToken.matches(KEYWORD,'or'):
            result, error = left.orBy(right)
        if error:
            return res.failure(error)
        else:
            return res.success(result.setPosition(node.posStart, node.posEnd))

    def visit_ifNode(self,node,context):
        res = runtimeResult()
        for condition,expr in node.case:
            conditionValue = res.register(self.visit(condition,context))
            if res.error:return res
            if conditionValue.isTrue():
                expressionValue = res.register(self.visit(expr,context))
                if res.error:return res
                return res.success(expressionValue)
        if node.elseCase:
            elseValue = res.register(self.visit(node.elseCase,context))
            if res.error:return res
            return res.success(elseValue)
        return res.success(None)

#Executable----------------------------------------------------------------------------------
staticSymbolTable = symbolTable()
staticSymbolTable.set("null",Number(0))
staticSymbolTable.set("true",Number(1))
staticSymbolTable.set("false",Number(0))

def run(text):
    lex = lexer(text)
    tokens, error = lex.makeTokens()
    if error: return None, error
    par = parser(tokens)
    tree = par.parse()
    if tree.error: return None, tree.error
    evaluate = eval()
    context = traceBackHandling('<program>')
    context.symbolTable = staticSymbolTable
    result = evaluate.visit(tree.node, context)
    return result.value, result.error


# Defining the shell function--------------------------------------------------------------------
def main():
    print("Welcome to Python 4! Where simplicity is actually true in this programming language.")
    while True:
        text = input('Result > ')
        result, error = run(text)
        if error:
            print(error.log())
        elif result:
            print(result)

if __name__ == "__main__":
    main()