#
# Product:   Macal
# Author:    Marco Caspers
# Date:      15-09-2022
#


import typing
import pathlib
import sys
import os

from . import __about__
from . import token
from . import ast
from . import ast_expr
from . import ast_function_definition
from . import ast_function_call
from . import ast_block
from . import ast_assignment
from . import ast_if
from . import ast_foreach
from . import ast_break
from . import ast_continue
from . import ast_halt
from . import ast_while
from . import ast_return
from . import ast_include
from . import ast_select_field
from . import ast_select
from . import mscope
from . import types
from . import exceptions
from . import value_item
from . import variable
from . import location



def ValidateFunctionArguments(func: ast_function_definition.FunctionDefinition, scope: mscope.Scope, filename: str) -> None:
    for arg in func.Arguments.Left:
        if arg.ExprType == types.ExprTypes.FunctionArgument:
            tok = arg.Left
        else:
            tok = arg.Token
        name = tok.Lexeme
        var = scope.FindVariable(name)
        if var is None:
            if arg.Token.Lexeme == 'params': return
            raise exceptions.RuntimeError(f'Function ({func.Name}) argument {arg.Token.Lexeme} not found.', tok.Location, filename)
        var.Token = tok
        if arg.ExprType == types.ExprTypes.FunctionArgument:
            t = var.GetType().lower()
            if tok.Lexeme != 'any' and tok.Lexeme != 'params' and tok.Lexeme != t:
                raise exceptions.RuntimeError(f'Invalid function ({func.Name}) argument type {t}, {tok.Lexeme} type was required.', arg.Token.Location, filename)


        
class Interpreter:
    def __init__(self, include: typing.Callable[[str, mscope.Scope], mscope.Scope]) -> None:
        self.filename: str = None
        self.Include: typing.Callable[[str, mscope.Scope], mscope.Scope] = include
        self.Halt: bool = False
        self.Source: str = None
        self.iter: int = 0
        self.INFINITE_LOOP_PROTECTION_COUNT: int = 25000 # limits a while loop to 25000 repeats before it gets terminated.



    def Interpret(self, source: typing.List[ast.AST], filename: str, scope: mscope.Scope) -> mscope.Scope:
        self.filename = filename
        scope.SetHalt(False)
        self.Source = source
        for instruction in source:
            self.InterpretInstruction(instruction, scope)
            if scope.Halt:
                return scope
        return scope



    def InterpretInstruction(self, instruction: ast.AST, scope: mscope.Scope) -> None:
        if instruction.Type == types.AstTypes.Assignment:
            return self.InterpretAssign(instruction, scope)
        if instruction.Type == types.AstTypes.Block:
            return self.InterpretBlock(instruction, scope)
        if instruction.Type == types.AstTypes.Break:
            return self.InterpretBreak(instruction, scope)
        if instruction.Type == types.AstTypes.Continue:
            return self.InterpretContinue(instruction, scope)
        if instruction.Type == types.AstTypes.FunctionCall:
            return self.RunFunctionCall(instruction, instruction.Args, instruction.Token, scope)
        if instruction.Type == types.AstTypes.FunctionDefinition:
            scope.Functions[instruction.Name] = instruction
            return
        if instruction.Type == types.AstTypes.If:
            return self.InterpretIf(instruction, scope)
        if instruction.Type == types.AstTypes.Include:
            return self.InterpretInclude(instruction, scope)
        if instruction.Type == types.AstTypes.Foreach:
            return self.InterpretForeach(instruction, scope)
        if instruction.Type == types.AstTypes.Halt:
            return self.InterpretHalt(instruction, scope)
        if instruction.Type == types.AstTypes.Return:
            return self.InterpretReturn(instruction, scope)
        if instruction.Type == types.AstTypes.Select:
            return self.InterpretSelect(instruction, scope)
        if instruction.Type == types.AstTypes.While:
            return self.InterpretWhile(instruction, scope)
        raise exceptions.RuntimeError(f"Invalid instruction type ({instruction.Type}).", instruction.Token.Location, self.filename)



    def InterpretInclude(self, instruction: ast_include.Include, scope: mscope.Scope) -> None:
        for include in instruction.Includes:
            incl = scope.FindInclude(include.Lexeme)
            if incl is not None: # already included
                continue
            (result, ex) = self.Include(include.Lexeme, scope)
            var = scope.Root.GetVariable('exitcode')
            if not result and ex is not None:
                var.SetValue(4)
                raise exceptions.RuntimeError(ex, instruction.Token.Location, self.filename)
            elif not result:
                var.SetValue(5)
                self.Halt = True



    def InterpretExpression(self, expr: ast.AST, scope: mscope.Scope) -> value_item.ValueItem:
        if expr is None:
            raise exceptions.RuntimeError("Invalid argument exception, expr is None.", None, self.filename)
        if expr.ExprType == types.ExprTypes.Literal:
            return self.InterpretLiteralExpression(expr, scope)
        if expr.ExprType == types.ExprTypes.Binary:
            return self.InterpretBinaryExpression(expr, scope)
        if expr.ExprType == types.ExprTypes.Unary:
            return self.InterpretUnaryExpression(expr, scope)
        if expr.ExprType == types.ExprTypes.Grouping:
            return self.InterpretExpression(expr.Left, scope)
        if expr.ExprType == types.ExprTypes.FunctionCall:
            return self.RunFunctionCallFromExpr(expr.Token.Lexeme, expr.Right.Left, expr.Right.Token, scope)
        if expr.ExprType == types.ExprTypes.FunctionArgument:
            raise exceptions.RuntimeError("Function Argument type should not end up in expression interpretation.", expr.Token.Location, self.filename)
        if expr.ExprType == types.ExprTypes.ArgumentList:
            raise exceptions.RuntimeError("Argument list type should not end up in expression interpretation.", expr.Token.Location, self.filename)
        if expr.ExprType == types.ExprTypes.Variable:
            return self.InterpretVariableExpression(expr, scope)
        if expr.ExprType == types.ExprTypes.VariableIndex:
            return self.InterpretLiteralExpression(expr.Left, scope)
        if expr.ExprType == types.ExprTypes.InterpolationPart:
            return self.InterpretBinaryExpression(expr.Right, scope)
        if expr.ExprType == types.ExprTypes.NewArrayIndex:
            return value_item.ValueItem().SetFromMacal(expr.Token, types.VariableTypes.NewArrayIndex, [])
        raise Exception("Expression type evaluation not implemented yet: ", expr.ExprType)



    def InterpretLiteralExpression(self, expr: ast.AST, scope: mscope.Scope) -> value_item.ValueItem:
        if expr is None: raise exceptions.RuntimeError("Invalid argument exception, expr is None.", None, self.filename)
        value = value_item.ValueItem()
        if expr.LiteralValueType == types.VariableTypes.Array:
            value.Token = expr.Token
            value.Type = expr.LiteralValueType
            value.Value = []
        elif expr.LiteralValueType == types.VariableTypes.Record:
            value.Token = expr.Token
            value.Type = expr.LiteralValueType
            value.Value = {}
        else:
            value.SetValue(expr.Token, expr.LiteralValueType, self.filename)
        return value



    def BinaryExpressionOperandsTypeCheck(self, left:value_item.ValueItem, right:value_item.ValueItem, op:str) -> None:
        if left is None or right is None: return
        # This is for catching bugs that cause left or right not to be of type ValueItem.
        if not isinstance(left, value_item.ValueItem):
            raise exceptions.RuntimeError(f'Binary Expression TypeCheck: Left is not a value item. ({type(left)})\n Left: {left}\n Right: {right}', right.Token.Location, self.filename)
        if not isinstance(right, value_item.ValueItem):
            raise exceptions.RuntimeError(f'Binary Expression TypeCheck: Right is not a value item. ({type(right)}) Left: {left}, Right: {right}', left.Token.Location, self.filename)
        if op == '$+': return
        if left.Type != right.Type:
            if (op == '==' or op == '!=') and (right.Type == types.VariableTypes.Bool or right.Type == types.VariableTypes.Nil or left.Type == types.VariableTypes.Nil or left.Type == types.VariableTypes.Bool):
                return
            if ((left.Type != types.VariableTypes.Int and left.Type != types.VariableTypes.Float) 
                 or (right.Type != types.VariableTypes.Int and right.Type != types.VariableTypes.Float)):
                raise exceptions.RuntimeError(f'Unsupported operand types for {op}. ({left.Type} and {right.Type})', left.Token.Location, self.filename)



    def InterpretBinaryExpression(self, expr: ast_expr.Expr, scope: mscope.Scope) -> value_item.ValueItem:
        left = self.InterpretExpression(expr.Left, scope)
        op = expr.Operator.Lexeme
        if op == 'and' and left.Value is False: return left
        if op == 'or' and left.Value is True: return left
        right = self.InterpretExpression(expr.Right, scope)
        if op == 'or' and right.Value is True: return right
        return self.ExecuteBinaryExpression(expr.Operator, left, right, op)
        


    def InterpretVariableExpression(self, expr: ast.AST, scope: mscope.Scope) -> value_item.ValueItem:
        var = scope.FindVariable(expr.Token.Lexeme)
        if var is None:
            var = scope.FindFunction(expr.Token.Lexeme, scope)
            if var is None: raise exceptions.RuntimeError(f'Variable or function ({expr.Token.Lexeme}) not found.', expr.Token.Location, self.filename)
            return value_item.ValueItem().SetFromMacal(expr.Token, types.VariableTypes.Function, var)
        var.Token = expr.Token
        if expr.Left is not None and expr.Left.ExprType == types.ExprTypes.VariableIndex: 
            index = self.InterpretIndex(expr.Left, scope)
            result = self.GetFromIndexed(var, index)
            if (((result.Type == types.VariableTypes.String or result.Type == types.VariableTypes.Array) and index[-1].Type != types.VariableTypes.Int)
                  or (result.Type == types.VariableTypes.Record and index[-1].Type != types.VariableTypes.String)):
                raise exceptions.RuntimeError(f'Invalid index type ({index[-1].Type}). ({var.Name}{self.IndexToString(index)}).', index[-1].Token.Location, self.filename)
            return result.Value[index[-1].Value]
        return var.Value
        


    def InterpretUnaryExpression(self, expr: ast_expr.Expr, scope: mscope.Scope) -> value_item.ValueItem:
        val = self.InterpretExpression(expr.Right, scope).Clone()
        if expr.Operator.Lexeme == '-': val.Value *= -1
        if expr.Operator.Lexeme == '!':
            if val.Type != types.VariableTypes.Bool: raise exceptions.RuntimeError(f"Invalid type ({val.Type}), not a boolean.", val.Token.Location, self.filename)
            val.Value = not val.Value
        return val



    def InterpretBlock(self, expr: ast_block.Block, scope: mscope.Scope) -> None:
        for instruction in expr.Instructions:
            self.InterpretInstruction(instruction, scope)
            if scope.Break or scope.Continue or scope.Return or scope.Halt: break



    def InterpretReturn(self, instruction: ast_return.Return, scope: mscope.Scope) -> None:
        if not scope.isFunction: raise exceptions.RuntimeError("Invalid return instruction outside function.",instruction.Token.Location, self.filename)
        returnVar = scope.GetVariable(f'?return_var{scope.Name}')
        returnVar.Value = self.InterpretExpression(instruction.Value, scope)
        scope.Return = True



    def HandleInfiniteLoopProtectionEmbeddedFunctions(self, func: ast_function_definition.FunctionDefinition, scope: mscope.Scope) -> value_item.ValueItem:
        if func.Name == 'setInfiniteLoopProtectionCount':
            var = scope.GetVariable('count')
            if var.GetType() != types.VariableTypes.Int:
                raise exceptions.RuntimeError(f"Function ({func.Name}) requires an integer value for the count argument.", func.Token.Location, self.filename)
            self.INFINITE_LOOP_PROTECTION_COUNT = var.GetValue()
        return value_item.ValueItem().SetFromMacal(func.Token, types.VariableTypes.Int, self.INFINITE_LOOP_PROTECTION_COUNT)



    def InterpretFunctionArgList(self, args: typing.List[ast_expr.Expr], funcArgs: typing.List[ast_expr.Expr], etoken: token.LexToken, fnName: str, scope: mscope.Scope, fnScope: mscope.Scope) -> None:
        i=0
        params = False
        name = None
        if len(args) == 0 and len(funcArgs) > 0 and funcArgs[0].Token.Lexeme != 'params':
            name = funcArgs[0].Token.Lexeme
            if name in ['string', 'int', 'float', 'array', 'record', 'type', 'variable']:
                name = funcArgs[0].Left.Lexeme
            else: raise exceptions.RuntimeError(f'Required function argument ({name}) missing. ({fnName})', etoken.Location, self.filename)
        for v in args:
            if i < len(funcArgs): a = funcArgs[i]
            else: raise exceptions.RuntimeError(f'Function argument count exceeded ({len(args)} found, {len(funcArgs)} expected). ({fnName})', v.Token.Location, self.filename)
            if a.Token.Lexeme == 'variable':
                arg = scope.NewVariable(a.Left, a.Left.Lexeme)
                fnScope.AddVariable(arg)
                if v.ExprType != types.ExprTypes.Variable:
                    raise exceptions.RuntimeError(f'Variable required as function argument. ({fnName})', v.Token.Location, self.filename)
                var = scope.FindVariable(v.Token.Lexeme)
                if var is None:
                    raise exceptions.RuntimeError(f'Variable ({v.Token.Lexeme}) not found. ({fnName})', v.Token.Location, self.filename)
                var.Token = v.Token
                var = var.Clone()
                val = self.InterpretExpression(v, scope)
                var.Token = v.Token
                var.Value = val
                arg.Value = value_item.ValueItem().SetFromMacal(v.Token, types.VariableTypes.Variable, var)
                i += 1
            else:
                val = self.InterpretExpression(v, scope)
                if params is False:
                    if a.ExprType == types.ExprTypes.Variable:
                        arg = fnScope.NewVariable(a.Token, a.Token.Lexeme)
                    else:
                        arg = fnScope.NewVariable(a.Left, a.Left.Lexeme)
                    fnScope.AddVariable(arg)
                    if a.Token.Lexeme == 'params':
                        params = True
                        v = value_item.ValueItem().SetFromMacal(a.Token, types.VariableTypes.Array, [])
                        v.Value.append(val)
                        arg.Value = v
                    else:
                        arg.Value = val
                        i += 1
                else: arg.Value.Value.append(val)



    def RunFunctionCallFromExpr(self, name: str, args: typing.List[ast_expr.Expr], tok: token.LexToken, scope: mscope.Scope) -> value_item.ValueItem:
        instruction = ast_function_call.FunctionCall(token.LexToken(name, types.LexTokenTypes.Identifier, tok.Location, -1), None)
        return self.RunFunctionCall(instruction, args, tok, scope)



    def RunFunctionCall(self, instruction: ast_function_call, args: typing.List[ast_expr.Expr], tok: token.LexToken, scope: mscope.Scope) -> value_item.ValueItem:
        name = instruction.Name
        func = scope.FindFunction(name, scope)
        if func is None:
            var = scope.FindVariable(name)
            if var is None:
                raise exceptions.RuntimeError(f"Function or variable ({name}) not found.", tok.Location, self.filename)            
            func = var.GetFunction()
            if func is None:
                raise exceptions.RuntimeError(f"Function ({name}) not found.", tok.Location, self.filename)
        fnScope = scope.CreateTempScope(f'fnCall.{func.Name}')
        fnScope.isFunction = True
        returnVar = fnScope.CreateAndAppendFunctionReturnVariable(tok)
        returnVar.Value = value_item.ValueItem().SetFromMacal(tok,types.VariableTypes.Nil, types.VariableTypes.Nil)
        self.InterpretFunctionArgList(args, func.Arguments.Left, tok, name, scope, fnScope)
        if func.IsExternal is False:
            ValidateFunctionArguments(func, fnScope, self.filename)
            self.InterpretBlock(func.Block, fnScope)
        elif func.Name == 'getInfiniteLoopProtectionCount' or func.Name == 'setInfiniteLoopProtectionCount':
            return self.HandleInfiniteLoopProtectionEmbeddedFunctions(func, fnScope)
        else:
            fnScope.RunFunction = self.RunFunction
            self.InterpretExternalFunction(func, fnScope)
        return returnVar.Value



    def RunFunction(self, funcName: str, scope: mscope.Scope, **kwargs) -> value_item.ValueItem:
        args = []
        func = scope.FindFunction(funcName, scope)
        if func is None:
            raise exceptions.RuntimeError(f'Function ({funcName}) not found.', None, None)
        if kwargs is not None and len(kwargs) > 0:
            for arg in func.Arguments.Left:
                if arg.ExprType == types.ExprTypes.FunctionArgument:
                    an = arg.Left.Lexeme
                else:
                    an = arg.Token.Lexeme
                if an in kwargs:
                    vi = value_item.ValueItem().SetFromPython(
                        token.LexToken(kwargs[an], types.LexTokenTypes.String, location.NullLoc(), -1),
                        kwargs[an])
                    if vi.Type == types.LexTokenTypes.String:
                        expr = ast_expr.Expr(token.LexToken(f'{kwargs[an]}', vi.Type, location.NullLoc(), -1))
                        expr.Type = vi.Type
                        expr.Left = vi
                    elif vi.Type == types.VariableTypes.Float or vi.Type == types.VariableTypes.Int:
                        expr = ast_expr.Expr(token.LexToken(f'{kwargs[an]}', types.LexTokenTypes.Number, location.NullLoc(), -1))
                        expr.Literal(vi.Type)
                        expr.Left = vi
                    elif vi.Type == types.VariableTypes.Bool:
                        expr = ast_expr.Expr(token.LexToken(f'{kwargs[an]}', types.LexTokenTypes.Identifier, location.NullLoc(), -1))
                        expr.Literal(vi.Type)
                        expr.Left = vi
                    elif isinstance(kwargs[an], variable.Variable):
                        expr = ast_expr.Expr(kwargs[an].Token).Variable(kwargs[an].Value.Type)
                    else:
                        raise exceptions.RuntimeError(f'Invalid argument type ({type(kwargs[an])}) in function ({funcName}).', None, None)
                    args.append(expr)
        result = self.RunFunctionCallFromExpr(funcName, args, 
            token.LexToken(funcName, types.LexTokenTypes.Identifier, location.NullLoc(), -1), scope)
        scope.SetReturnValue(result.Value)
        return result.Value



    def FindModuleFilePath(self, module: str, scope: mscope.Scope):
        fileName = f'{module}.py'
        path = os.path.join(os.path.dirname(__file__), "Library", "Extern", fileName)
        fp = pathlib.Path(path).parent
        if pathlib.Path(path).is_file(): return str(fp)
        path = f'{scope.externFolder}/{fileName}'
        fp = pathlib.Path(path).parent
        if pathlib.Path(path).is_file(): return str(fp)
        fp = os.path.join(pathlib.Path(self.filename).parent.absolute())
        path = f'{str(fp)}/{fileName}'
        if pathlib.Path(path).is_file(): return fp
        return None



    def LoadModule(self, modulename, functionname, scope: mscope.Scope):
        filepath = self.FindModuleFilePath(modulename, scope)
        if filepath is None: return None
        if filepath not in sys.path:
            sys.path.insert(0, filepath)
        module = __import__(modulename, locals(), globals() , [functionname])
        return module



    def InterpretExternalFunction(self, func: ast_function_definition.FunctionDefinition, scope: mscope.Scope) -> value_item.ValueItem:
        module = self.LoadModule(func.ExternalModule.Lexeme, func.ExternalFunction.Lexeme, scope)
        if module is None:
            raise exceptions.RuntimeError(f"Function ({func.Name}) not found.", func.Token.Location, self.filename)
        fn = getattr(module, func.ExternalFunction.Lexeme)
        fn(func, scope, self.filename)
        exitVar = scope.GetVariable(f'?return_var{scope.Name}')
        return exitVar.Value



    def InterpretBreak(self, instruction: ast_break.Break, scope: mscope.Scope) -> None:
        if not scope.isLoop: raise exceptions.RuntimeError("Invalid break instruction outside loop.", instruction.Token.Location, self.filename)
        scope.Break = True
        pscope = scope
        while pscope.isLoopRoot is False:
            pscope = pscope.Parent
            pscope.Break = True



    def InterpretContinue(self, instruction: ast_continue.Continue, scope: mscope.Scope) -> None:
        if not scope.isLoop: raise exceptions.RuntimeError("Invalid continue instruction outside loop.",instruction.Token.Location, self.filename)
        scope.Continue = True
        pscope = scope
        while pscope.isLoopRoot is False and pscope.Parent is not None:
            pscope = pscope.Parent
            pscope.Continue = True



    def InterpretHalt(self, instruction: ast_halt.Halt, scope: mscope.Scope) -> None:
        value = self.InterpretExpression(instruction.Exitcode, scope)
        var = scope.Root.GetVariable('exitcode')
        var.Value = value
        scope.SetHalt(True)


    
    def InterpretForeach(self, instruction: ast_foreach.Foreach, scope: mscope.Scope) -> None:
        val = self.InterpretExpression(instruction.Variable, scope)
        fes = scope.CreateTempScope('foreach')
        fes.isLoop = True
        fes.isLoopRoot = True
        it = fes.NewVariable(instruction.Variable.Token, 'it')
        fes.AddVariable(it)
        if val.Type == types.VariableTypes.String or val.Type == types.VariableTypes.Record:
            for v in val.Value:
                vv = value_item.ValueItem().SetFromMacal(instruction.Variable.Token, types.VariableTypes.String, v)
                if fes.Break or fes.Halt or fes.Return: break
                fes.Continue = False
                it.Value = vv
                self.InterpretBlock(instruction.Block, fes)
        else:
            for v in val.Value:
                v.Token = instruction.Variable.Token
                if fes.Break or fes.Halt or fes.Return: break
                fes.Continue = False
                it.Value = v
                self.InterpretBlock(instruction.Block, fes)
        

    
    def InterpretWhile(self, instruction: ast_while.While, scope: mscope.Scope) -> None:
        whs = scope.CreateTempScope('while')
        whs.isLoop = True
        whs.isLoopRoot = True
        if self.INFINITE_LOOP_PROTECTION_COUNT == 0:
            self.InterpretWhileWithoutLoopProtection(instruction, scope, whs)
        else:
            self.InterpretWhileWithLoopProtection(instruction, scope, whs)



    def InterpretWhileWithLoopProtection(self, instruction: ast_while.While, scope: mscope.Scope, block_scope: mscope.Scope) -> None:
        infiniteLoopProtection = self.INFINITE_LOOP_PROTECTION_COUNT
        condition = self.InterpretExpression(instruction.condition, scope)
        while condition.Value is True and infiniteLoopProtection > 0:
            if scope.Break or scope.Halt or scope.Return: break
            scope.Continue = False
            self.InterpretBlock(instruction.Block, block_scope)
            condition = self.InterpretExpression(instruction.Condition, scope)
            infiniteLoopProtection -= 1
        if infiniteLoopProtection == 0:
            raise exceptions.RuntimeError("Infinite loop protection engaged.", instruction.Token.Location, self.filename)



    def InterpretWhileWithoutLoopProtection(self, instruction: ast_while.While, scope: mscope.Scope, block_scope: mscope.Scope) -> None:
        condition = self.InterpretExpression(instruction.condition, scope)
        while condition.Value is True:
            if scope.Break or scope.Halt or scope.Return: break
            scope.Continue = False
            self.InterpretBlock(instruction.Block, block_scope)
            condition = self.InterpretExpression(instruction.Condition, scope)



    def InterpretIf(self, instruction: ast_if.If, scope: mscope.Scope) -> None:
        condition = self.InterpretExpression(instruction.Condition, scope)
        if condition.Value is True: 
            self.InterpretBlock(instruction.Block, scope.CreateTempScope('if'))
            return
        if len(instruction.Elif) > 0:
            for elfi in instruction.Elif:
                lifs = scope.CreateTempScope('elif')
                condition = self.InterpretExpression(elfi.Condition, lifs)
                if condition.Value is True:
                    self.InterpretBlock(elfi.Block, lifs)
                    return
        if instruction.Else is not None:
            self.InterpretBlock(instruction.Else, scope.CreateTempScope('else'))



    def InterpretSelect(self, instruction: ast_select.Select, scope: mscope.Scope) -> None:
        data = self.InterpretExpression(instruction.From, scope)
        into = self.EvaluateIntoVariable(instruction.Into, scope)
        if into is None:
            if instruction.Merge is True:
                raise exceptions.RuntimeError(f'Variable ({instruction.Into.Token.Lexeme}) not found.', instruction.Into.Token.Location, self.filename)
            intoVar = variable.Variable(instruction.Into.Token, instruction.Into.Token.Lexeme)
            if instruction.Distinct:
                intoVar.Value = value_item.ValueItem().SetFromMacal(instruction.Token, types.VariableTypes.Record, {})
            else:
                intoVar.Value = value_item.ValueItem().SetFromMacal(instruction.Token, types.VariableTypes.Array, [])
            scope.AddVariable(intoVar)
            into = intoVar.Value      
        if instruction.Where is not None and data is not None:
            data = self.InterpretSelectWhere(instruction.Where, data, scope)
        if not(len(instruction.Fields) == 1 and instruction.Fields[0].Name == '*'):
            data = self.ApplyFieldFilters(data, instruction.Fields)
        if instruction.Distinct is True and data is not None and data.Type == types.VariableTypes.Array and len(data.Value) > 0:
            if isinstance(data.Value[0], value_item.ValueItem):
                data = data.Value[0]
            else:
                raise exceptions.RuntimeError(f'Debug Select (distinct): data.Value[0] is NOT ValueItem but it should!', data.Token.Location, self.filename)    
        if data is not None and data.Type == types.VariableTypes.Array and len(data.Value) == 1:
            data = data.Value[0]
        if instruction.Merge is True and data is not None:
            data = self.InterpretSelectMerge(into, data)
        # second time is needed, just in case merge returns an array of 1 record..
        if data is not None and data.Type == types.VariableTypes.Array and len(data.Value) == 1:
            data = data.Value[0]
        if data is not None:
            self.SetIntoVariableValue(instruction.Into, data, scope)



    def SetIntoVariableValue(self, expr: ast_expr.Expr, data: value_item.ValueItem, scope: mscope.Scope) -> None:
        var = scope.FindVariable(expr.Token.Lexeme)
        if var is None:
            raise exceptions.RuntimeError(f'Variable ({expr.Token.Lexeme}) not found.', expr.Token.Location, self.filename)
        var.Token = expr.Token
        if expr.Left is None:
            var.Value = data
            return
        if expr.Left.ExprType == types.ExprTypes.VariableIndex:
            self.AssignToIndexed(var, expr.Left, data, False, scope)
            return
        raise exceptions.RuntimeError(f'Variable ({expr.Token.Lexeme}) has an invalid left hand expression type: {expr.Left.ExprType}.', expr.Token.Location, self.filename)



    def GetEmptyRecord(self, fields: typing.List[ast_select_field.SelectField]) -> value_item.ValueItem:
        return_data = value_item.ValueItem().SetFromMacal(token.LexToken.NullToken(), types.VariableTypes.Record, {})
        for fld in fields:
            return_data.Value[fld.AsName] = value_item.ValueItem().SetFromMacal(fld.Token, types.VariableTypes.Nil, types.VariableTypes.Nil)
        return return_data


    def GetRecordData(self, fields: typing.List[ast_select_field.SelectField], data: value_item.ValueItem) -> value_item.ValueItem:
        r = value_item.ValueItem().SetFromMacal(data.Token, types.VariableTypes.Record, {})
        for fld in fields:
            if fld.Name in data.Value:
                r.Value[fld.AsName] = data.Value[fld.Name]
            else:
                r.Value[fld.AsName] = value_item.ValueItem().SetFromMacal(fld.Token, types.VariableTypes.Nil, types.VariableTypes.Nil)
        return r


    def ApplyFieldFilters(self, data: value_item.ValueItem, fields: typing.List[ast_select_field.SelectField]) -> value_item.ValueItem:
        # in select we already gate for * as field, so we don't have to check for that.
        if data is None: return self.GetEmptyRecord(fields)
        elif data.Type == types.VariableTypes.Array:
            if len(data.Value) == 0: return self.GetEmptyRecord(fields)
            return_data = value_item.ValueItem().SetFromMacal(data.Token, data.Type, [])
            for rec in data.Value:
                r = self.GetRecordData(fields, rec)
                return_data.Value.append(r)
            return return_data
        elif data.Type == types.VariableTypes.Record:
            return self.GetRecordData(fields, data)
        return data



    def InterpretSelectWhere(self, expr: ast_expr.Expr, data: value_item.ValueItem, scope:mscope.Scope)-> value_item.ValueItem:
        if data.Type == types.VariableTypes.Array:
            returnData = value_item.ValueItem().SetFromMacal(data.Token, data.Type, [])
            for rec in data.Value:
                res = self.EvaluateDatafieldExpression(expr, rec, scope)
                if res.Value is True: 
                    returnData.Value.append(rec)
            return returnData
        returnData = value_item.ValueItem().SetFromMacal(data.Token, types.VariableTypes.Record, {})
        self.EvaluateDatafieldExpression(expr, data, scope)
        if res.Value is True: returnData = data
        return returnData
        


    def InterpretSelectMerge(self, into: value_item.ValueItem, data: value_item.ValueItem)-> value_item.ValueItem:
        if (into.Type == types.VariableTypes.Record and data.Type == types.VariableTypes.Record):
            if set(into.Value.keys()) == set(data.Value.keys()):
                returnData = value_item.ValueItem().SetFromMacal(into.Token, types.VariableTypes.Array, [])
                returnData.Value.append(into)
                returnData.Value.append(data)
                return returnData
            else:
                returnData = into
                for key, value in data.Value.items():
                    returnData.Value[key] = value
                return returnData
        returnData = value_item.ValueItem().SetFromMacal(into.Token, types.VariableTypes.Array, [])
        if into.Type == types.VariableTypes.Array:
            for rec in into.Value:
                returnData.Value.append(rec)
        # Into can be nil here, so we must check.
        elif into.Type == types.VariableTypes.Record:
            returnData.Value.append(into)
        if data.Type == types.VariableTypes.Array:
            for rec in data.Value:
                returnData.Value.append(rec)
        elif data.Type == types.VariableTypes.Record:
            returnData.Value.append(data)
        return returnData



    def EvaluateDatafieldExpression(self, expr: ast_expr.Expr, rec: value_item.ValueItem, scope: mscope.Scope) -> value_item.ValueItem:
        if expr.ExprType == types.ExprTypes.Variable: return self.EvaluateDatafieldVariable(expr, rec, scope)
        if expr.ExprType == types.ExprTypes.Literal: return self.EvaluateDatafieldLiteral(expr, rec, scope)
        if expr.ExprType == types.ExprTypes.Binary: return self.EvaluateDatafieldBinary(expr, rec, scope)
        if expr.ExprType == types.ExprTypes.Unary: return self.EvaluateDatafieldUnary(expr, rec, scope)
        if expr.ExprType == types.ExprTypes.Grouping: return self.EvaluateDatafieldExpression(expr.Left, rec, scope)
        raise exceptions.RuntimeError(f'Invalid datafield expression type ({expr.ExprType}).', expr.Token.Location, self.filename)



    def EvaluateDatafieldLiteral(self, expr: ast_expr.Expr, rec: value_item.ValueItem, scope: mscope.Scope) -> value_item.ValueItem:
        value = value_item.ValueItem()
        if expr.LiteralValueType == types.VariableTypes.Array:
            value.Token = expr.Token
            value.Type = expr.LiteralValueType
            value.Value = []
        elif expr.LiteralValueType == types.VariableTypes.Record:
            value.Token = expr.Token
            value.Type = expr.LiteralValueType
            value.Value = {}
        else:
            value.SetValue(expr.Token, expr.LiteralValueType, self.filename)
        return value



    def EvaluateDatafieldBinary(self, expr: ast_expr.Expr, rec: value_item.ValueItem, scope: mscope.Scope) -> value_item.ValueItem:
        left = self.EvaluateDatafieldExpression(expr.Left, rec, scope)
        op = expr.Operator.Lexeme
        if op == 'and' and left.Value is False: return left
        if op == 'or' and left.Value is True: return left
        right = self.EvaluateDatafieldExpression(expr.Right, rec, scope)
        if op == 'or' and right.Value is True: return right
        return self.ExecuteBinaryExpression(expr.Operator, left, right, op)



    def ExecuteBinaryExpression(self, tok: token.LexToken, left: value_item.ValueItem, right: value_item.ValueItem, op: str) -> value_item.ValueItem:
        self.BinaryExpressionOperandsTypeCheck(left, right, op)
        if op == "+": return left + right
        if op == "-": return left - right
        if op == "/": return left / right
        if op == "*": return left * right
        if op == "^": return left ** right
        if op == "%": return left % right
        if op == ">": return left > right
        if op == "<": return left < right
        if op == ">=": return left >= right
        if op == "<=": return left <= right
        if op == "!=": return left != right
        if op == "==": return left == right
        if op == "and": return left and right
        if op == "or": return left or right
        if op == "$+":
            res = value_item.ValueItem()
            res.Type = types.VariableTypes.String
            res.Token = left.Token
            res.Value = f'{left.Value}{right.Value}'
            return res
        raise exceptions.RuntimeError("Unknown operator, expr is None.", tok.Location, self.filename)



    def EvaluateDatafieldVariable(self, expr: ast_expr.Expr, rec: value_item.ValueItem, scope: mscope.Scope) -> value_item.ValueItem:
        if rec.Type == types.VariableTypes.Record and expr.Token.Lexeme in rec.Value:
            return rec.Value[expr.Token.Lexeme]
        val = self.EvaluateIntoVariable(expr, scope)
        if val is None:
            raise exceptions.RuntimeError(f'Variable ({expr.Token.Lexeme}) not found.', expr.Token.Location, self.filename)
        return val
        


    def EvaluateIntoVariable(self, expr: ast_expr.Expr, scope: mscope.Scope) -> value_item.ValueItem:
        var = scope.FindVariable(expr.Token.Lexeme)
        if var is None:
            return None
        var.Token = expr.Token
        if expr.Left is None:
            return var.Value
        if expr.Left.ExprType == types.ExprTypes.VariableIndex:
            index = self.InterpretIndex(expr.Left, scope)
            result = self.GetFromIndexed(var, index)
            if (((result.Type == types.VariableTypes.String or result.Type == types.VariableTypes.Array) and index[-1].Type != types.VariableTypes.Int)
                  or (result.Type == types.VariableTypes.Record and index[-1].Type != types.VariableTypes.String)):
                raise exceptions.RuntimeError(f'Invalid index type ({index[-1].Type}). ({var.Name}{self.IndexToString(index)}).', index[-1].Token.Location, self.filename)
            return result.Value[index[-1].Value]
        raise exceptions.RuntimeError(f'Variable ({expr.Token.Lexeme}) has an invalid left hand expression type: {expr.Left.ExprType}.', expr.Token.Location, self.filename)



    def EvaluateDatafieldUnary(self, expr: ast_expr.Expr, rec: dict, scope: mscope.Scope) -> value_item.ValueItem:
        val = self.EvaluateDatafieldExpression(expr.Right, rec, scope).Clone()
        if expr.Operator.Lexeme == '-':
            val.Value *= -1
        if expr.Operator.Lexeme == '!':
            if val.Type != types.VariableTypes.Bool:
                raise exceptions.RuntimeError(f"Invalid type ({val.Type}), not a boolean.", val.Token.Location, self.filename)
            val.Value = not val.Value
        return val



    def InterpretIndex(self, index: ast_expr.Expr, scope: mscope.Scope) -> typing.List[value_item.ValueItem]:
        if index is None:
            raise exceptions.RuntimeError(f"Invalid nil index.", None, self.filename)
        vind = []
        for idx in index.Left:
            vind.append(self.InterpretExpression(idx, scope))
        return vind


    @staticmethod
    def IndexToString(index: typing.List[value_item.ValueItem]) -> str:
        s = ""
        for idx in index:
            if idx.Type == types.VariableTypes.NewArrayIndex:
                s = f"{s}[]"
            else:
                s = f"{s}[{idx.Value}]"
        return s



    def WalkIndex(self, value: value_item.ValueItem, index: typing.List[value_item.ValueItem], length: int, name: str) -> value_item.ValueItem:
        i = 0
        idx = index[i]
        while i < length - 1:
            if value.Type not in [types.VariableTypes.String, types.VariableTypes.Record, types.VariableTypes.Array]:
                raise exceptions.RuntimeError(f'Non indexable value. ({name}{self.IndexToString(index)}', value.Token.Location, self.filename)           
            if idx.Type == types.VariableTypes.NewArrayIndex:
                return value
            if value.Type == types.VariableTypes.Record:
                if i < length - 2:
                    raise exceptions.RuntimeError(f'Invalid record index. ({name}{self.IndexToString(index)}', value.Token.Location, self.filename)           
                if idx.Value not in value.Value: return value
            if (((value.Type == types.VariableTypes.String or value.Type == types.VariableTypes.Array) and idx.Type != types.VariableTypes.Int) 
                    or (value.Type == types.VariableTypes.Record and idx.Type != types.VariableTypes.String)):
                raise exceptions.RuntimeError(f'Invalid index type ({idx.Type}). ({name}{self.IndexToString(index)}', value.Token.Location, self.filename)
            value = value.Value[idx.Value]
            i+=1
            idx = index[i]
        return value



    def GetFromIndexed(self, var: variable.Variable, index: typing.List[value_item.ValueItem])-> value_item.ValueItem:
        l = len(index)
        if l > 0:
            result = self.WalkIndex(var.Value, index, l, var.Name)
        else:
            result = var.Value
        return result



    def InterpretAssign(self, instruction: ast_assignment.Assignment, scope: mscope.Scope) -> None:
        var = scope.FindVariable(instruction.Variable)
        if var is None:
            var = scope.NewVariable(instruction.Token, instruction.Variable)
            var.isConst = instruction.isConst
            scope.AddVariable(var)
        elif var.isConst:
            raise exceptions.RuntimeError(f'Illegal assignment to a constant ({instruction.Variable}).', instruction.Token.Location, self.filename)
        else:
            var.Token = instruction.Token
        value = self.InterpretExpression(instruction.Value, scope)
        if instruction.VarIndex is not None:
            return self.AssignToIndexed(var, instruction.VarIndex, value, True, scope)
        if instruction.Operator.Lexeme == '=': var.Value = value.Clone()
        elif instruction.Operator.Lexeme == '+=': var.Value = var.Value + value
        elif instruction.Operator.Lexeme == '-=': var.Value = var.Value - value
        elif instruction.Operator.Lexeme == '/=': var.Value = var.Value / value
        elif instruction.Operator.Lexeme == '*=': var.Value = var.Value * value
        else: raise exceptions.RuntimeError(message = f'Invalid instruction assign operator: {instruction.Operator.Lexeme}', location=instruction.Token.Location, filename=self.filename)



    def AssignToIndexed(self, var: variable.Variable, index_expr: ast_expr.Expr, value: value_item.ValueItem, can_append: bool, scope: mscope.Scope) -> None:
        index = self.InterpretIndex(index_expr, scope)
        result = self.GetFromIndexed(var, index)
        if index[-1].Type == types.VariableTypes.NewArrayIndex:
            if result.Type != types.VariableTypes.Array or can_append == False:
                raise exceptions.RuntimeError(f'Append not supported. ({var.Name}{self.IndexToString(index)}', value.Token.Location, self.filename)
            result.Value.append(value)
            return
        result.Value[index[-1].Value] = value
