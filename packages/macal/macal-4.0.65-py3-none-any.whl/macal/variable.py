#
# Product:   Macal
# Author:    Marco Caspers
# Date:      15-09-2022
#

from __future__ import annotations
import copy
import typing
from . import types
from . import token
from . import value_item
from . import exceptions
from . import ast_function_definition


class Variable:
    def __init__(self, tok: token.LexToken, name: str) -> None:
        self.Token: token.LexToken = tok
        self.Name: str = name
        self.Value: value_item.ValueItem = None
        self.isConst: bool = False


    
    def GetValue(self) -> typing.Any:
        if self.Value is None:
            print("Debug: variable.getValue: self.Value is None.")
            return None
        if self.Value.Type in [types.VariableTypes.String, types.VariableTypes.Int, types.VariableTypes.Float, types.VariableTypes.Bool, types.VariableTypes.Nil, types.VariableTypes.Variable]:
            return self.Value.Value
        if self.Value.Type == types.VariableTypes.Record:
            return self.MacalRecordToPythonValue(self.Value)
        if self.Value.Type == types.VariableTypes.Array:
            return self.MacalArrayToPythonValue(self.Value)
        if self.Value.Type == types.VariableTypes.Function:
            return self.MacalFunctionToPythonValue(self.Value)
        if self.Value.Type == types.VariableTypes.Type:
            return self.MacalTypeToPythonValue(self.Value)
        raise exceptions.RuntimeError(f"getValue() for type {self.Value.Type} Not implemented.", self.Token.Location, None)



    def GetFunction(self) -> ast_function_definition.FunctionDefinition:
        if self.Value.Type == types.VariableTypes.Function:
            return self.Value.Value
        return None



    def MacalRecordToPythonValue(self, val: value_item.ValueItem) -> typing.Any:
        res = {}
        check = [types.VariableTypes.String, types.VariableTypes.Int, types.VariableTypes.Float, types.VariableTypes.Bool, types.VariableTypes.Nil]
        for (k, v) in val.Value.items():
            if v.Type in check:
                res[k] = v.Value
            elif v.Type == types.VariableTypes.Record:
                res[k] = self.MacalRecordToPythonValue(v)
            elif v.Type == types.VariableTypes.Array:
                res[k] = self.MacalArrayToPythonValue(v)
            elif v.Type == types.VariableTypes.Function:
                res[k] = self.MacalFunctionToPythonValue(v)
            elif v.Type == types.VariableTypes.Type:
                res[k] = self.MacalTypeToPythonValue(v)
            else:
                raise exceptions.RuntimeError(f"getValue() for type {v.Type} Not implemented.", v.Token.Location, None)
        return res



    def MacalFunctionToPythonValue(self, val: value_item.ValueItem) -> str:
        func = val.Value
        params = ', '.join([f'{arg.Token.Lexeme}' for arg in func.Arguments])
        return f'<Macal function: {func.Name}({params})>'



    def MacalArrayToPythonValue(self, val: value_item.ValueItem) -> typing.Any:
        res = []
        for v in val.Value:
            if v.Type in [types.VariableTypes.String, types.VariableTypes.Int, types.VariableTypes.Float, types.VariableTypes.Bool, types.VariableTypes.Nil]:
                res.append(v.Value)
            elif v.Type == types.VariableTypes.Record:
                res.append(self.MacalRecordToPythonValue(v))
            elif v.Type == types.VariableTypes.Array:
                res.append(self.MacalArrayToPythonValue(v))
            elif v.Type == types.VariableTypes.Function:
                res.append(self.MacalFunctionToPythonValue(v))
            elif v.Type == types.VariableTypes.Type:
                res.append(self.MacalTypeToPythonValue(v))
            else:
                raise exceptions.RuntimeError(f"getValue() for type {v.Type} Not implemented.", v.Token.Location, None)
        return res



    def GetType(self) -> types.VariableType:
        if self.Value is None:
            print("Debug: variable.getType(): self.Value is None.")
            return None
        return self.Value.Type



    def SetValue(self, value: typing.Any) -> None:
        if self.Value is None:
            print("Debug: variable.setValue: self.Value is None.")
            return None
        self.Value = self.Value.SetFromPython(self.Token, value)        



    def MacalTypeToPythonValue(self, val: types.VariableTypes.Type) -> str:
        return f'<Macal type: {val.Value}>'



    def __repr__(self) -> str:
        return self.__str__()



    def __str__(self) -> str:
        return f'{self.Name} = {self.Value}'



    def Clone(self):
        return copy.deepcopy(self)