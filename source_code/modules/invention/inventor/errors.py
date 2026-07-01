class SasSyntaxError(Exception):
    def __init__(self, message: str, line: int, column: int, context: str):
        self.message = message
        self.line = line
        self.column = column
        self.context = context
        super().__init__(f"Structure Syntax Error:\n{message}\nLocation: Line {line}, Column {column}\nContext: {context}")

class SasSemanticError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Signature Semantic Error:\n{message}")

class ImplSyntaxError(Exception):
    def __init__(self, id: str, message: str, line: int, column: int, context: str):
        self.id = id
        self.message = message
        self.line = line
        self.column = column
        self.context = context
        super().__init__(f"Implementation Syntax Error for {id}:\n{message}\nLocation: Line {line}, Column {column}\nContext: {context}")

class ImplSemanticError(Exception):
    def __init__(self, message: str, id: str = None, line: int = None, column: int = None, context: str = None):
        self.message = message
        self.id = id
        self.line = line
        self.column = column
        self.context = context
        
        if id is not None and line is not None and column is not None and context is not None:
            super().__init__(f"Implementation Semantic Error for {id}:\n{message}\nLocation: Line {line}, Column {column}\nContext: {context}")
        else:
            super().__init__(f"Implementation Semantic Error:\n{message}")