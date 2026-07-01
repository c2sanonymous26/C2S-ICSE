from pydantic import BaseModel, Field, model_validator
from typing import Any, Type, Optional

# Create a common validator function to handle all str type fields
def strip_str_fields(model_cls: Type[BaseModel]):
    @model_validator(mode='before')
    @classmethod
    def _strip_str_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for field_name, field_value in data.items():
                if isinstance(field_value, str):
                    data[field_name] = field_value.strip()
                elif isinstance(field_value, list) and any(isinstance(item, str) for item in field_value):
                    # Process each element in the list, apply strip only to string types
                    data[field_name] = [
                        item.strip() if isinstance(item, str) else item 
                        for item in field_value
                    ]
        return data
    
    # Add validator to model class
    setattr(model_cls, '_strip_str_fields', _strip_str_fields)
    return model_cls

# ---- Phase 1 Response Model ----
@strip_str_fields
class Intent(BaseModel):
    content: str = Field(..., description="What the constraint checks.")
    goal: str = Field(..., description="What the purpose of the constraint is.")
    design_rationale: str = Field(..., description="Why the constraint is designed this way for this specific scenario.")

@strip_str_fields
class IntentAndSemantics(BaseModel):
    intent: Intent = Field(..., description="The intent of the constraint.")
    semantics: str = Field(..., description="The semantics of the constraint expressed using logical anchors.")

# ---- Phase 2 Response Model ----
@strip_str_fields
class BfuncSignature(BaseModel):
    id: str = Field(..., description="The id of the bfunc, in the format of bfunc<j>.")
    parameters: list[str] = Field(..., description="The parameters of the bfunc.")
    semantics: str = Field(..., description="The semantics of the bfunc.")

@strip_str_fields
class StructureAndSignatures(BaseModel):
    structure: Optional[str] = Field(default=None, description="The structure of the template following the BNF grammar defined in the prompt. (Optional)")
    signatures: Optional[list[BfuncSignature]] = Field(default=None, description="A list of bfunc signatures in the structure. (Optional)")

# ---- Phase 3 Response Model ----
@strip_str_fields
class BfuncBody(BaseModel):
    id: str = Field(..., description="The id of the bfunc, in the format of bfunc<j>.")
    implementation: str = Field(..., description="The implementation of the bfunc")

@strip_str_fields
class BfuncImplementationNoCheck(BaseModel): 
    bodies: Optional[list[BfuncBody]] = Field(default=None, description="A list of bfunc implementations. (Optional)")

@strip_str_fields
class BfuncImplementationWithCheck(BaseModel):
    bodies: Optional[list[BfuncBody]] = Field(default=None, description="A list of bfunc implementations. (Optional)")
    reason: Optional[str] = Field(default=None, description="The reason why to regenerate structures and signatures. (Optional)")

# ---- Phase 4 Response Model ----
@strip_str_fields
class SymbolRestriction(BaseModel):
    symbol: str = Field(..., description="The symbol to be restricted.")
    restriction: str = Field(..., description="The restriction for the symbol.")

@strip_str_fields
class SymbolRestrictions(BaseModel):
    restrictions: Optional[list[SymbolRestriction]] = Field(default=None, description="A list of symbol restrictions.")

# ---- Final Response Model ----
@strip_str_fields
class Bfunc(BaseModel):
    id: str = Field(..., description="The id of the bfunc, in the format of bfunc<j>.")
    parameters: list[str] = Field(..., description="The parameters of the bfunc.")
    semantics: str = Field(..., description="The semantics of the bfunc.")
    implementation: str = Field(..., description="The implementation of the bfunc")
    restrictions: list[str] = Field(..., description="The restrictions of the bfunc.")

@strip_str_fields
class Template(BaseModel):
    intent: Intent = Field(..., description="The intent of the template.")
    semantics: str = Field(..., description="The semantics of the template.")
    structure: str = Field(..., description="The structure of the template.")
    bfuncs: list[Bfunc] = Field(..., description="A list of bfuncs in the template.")
