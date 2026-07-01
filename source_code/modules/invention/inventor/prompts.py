# ---- Structured Output Error Prompt ----
STRUCTURED_OUTPUT_ERROR_PROMPT = """
Your output is not valid! 
Your output should confirm to the JSON Schema and can be parsed by `json.loads`!
Please fix the errors!
"""

# ---- System Prompt ----
AGENT_DISCRIPTION_SCOPE = """
You are tasked with creating a constraint for a given software execution scenario.

In such a scenario, the system models its environment status (e.g., sensor measurements) as contexts and collects them during execution, where each context is a timestamped data record capturing the system's observed state at a specific moment. The collection of these contexts forms a context sequence. The constraint is a logical statement (corresponding to a first-order logic formula) that reflects properties of individual contexts or relations among different contexts in the context sequence. The constraint must have practical physical meaning and be logically reasonable, and should be tailored to the specific scenario.

To accomplish this, you will be provided with four key pieces of information:

1. The introduction of the scenario. It will be enclosed in <scenario> tags in the user's message.

2. The metadata of the context sequence including description, schema, and fields' explanations, which will be enclosed in <context_definitions> tags in the user's message.

3. The scope of the constraint (a.k.a, what kind of properties the constraint should or should not reflect), which will be enclosed in <scope> tags in the user's message.

4. A list of existing constraints (actually the semantics of the constraints) that you should avoid duplicating, which will be enclosed in <existing_semantics> tags in the user's message.

A well-formed constraint consists of an intent, semantics, a structure, and a list of bfuncs (boolean expressions as the predicates of the constraint).

The process of creating a constraint consists of three phases:
1. Identify the constraint intent and semantics in natural language (English). The intent articulates the content (what the constraint checks), goal (what the purpose of the constraint is), and design rationale (why the constraint is designed this way). The semantics, derived from the intent, should clearly describe the logical relationships between contexts and can be mapped to first-order logic formulas.
2. Convert the natural language semantics into a formal logical structure and decompose it into a list of bfunc signatures. This phase ensures that the constraint can be properly formalized and that each bfunc can be computed using only the contexts introduced in the structure.
3. Implement each bfunc based on its signature, ensuring that the implementation accurately reflects the intended semantics and can be computed using the available contexts.

In each phase, you should think carefully and follow the user's instructions to create a well-formed constraint.
"""

# ---- Phase 1 Prompt ----
PHASE1_USER_PROMPT_TEMPLATE_SCOPE = """
Here are the four key pieces of information:

<scenario>
{{scenario}}
</scenario>

<context_definitions>
Description: {{ctx_definitions.description}}
Schema:  
| field name | description | type | unit |
|------------|-------------|------|------|
{% for name, info in ctx_definitions.fields.items() %}
| {{ name }} | {{ info.get('description', '') | replace('|', '\\|') }} | {{ info.get('type', '') }} | {{ info.get('unit', 'String type has no unit') }} |
{% endfor %}
{{ ctx_definitions.explanation }}
</context_definitions>

<scope>
{{scope}}
</scope>

<existing_semantics>
{% for semantics in existing_semantics %}
- {{ semantics }}
{% endfor %}
</existing_semantics>

The Phase 1 is to generate the intent and semantics by following the requirements below.

1. First, identify the constraint intent in English. The intent should articulate: the content (what the constraint checks), the goal (what the purpose of the constraint is), and the design rationale (why the constraint is designed this way for this specific scenario).

2. Then, express the semantics in English clearly and concisely based on the intent. Ensure the semantics can be clearly mapped to first-order logic formulas. Use logical structures (i.e., "for any...", "there exists... such that", "if... then...", "and", "or", "not") to express relationships to facilitate accurate conversion into formalized constraint structures later. Do not use "if... then..." unless it is absolutely necessary.

3. Contexts can ONLY be introduced through quantifiers (i.e., "for any..." or "there exists... such that"), for example, "for any two contexts..." or "there exists a context such that...". Other logical structures ("if... then...", "and", "or", "not") are ONLY used to connect parts. Remember to quantify over contexts themselves, not the real-world entities that generate them (e.g., quantify over 'contexts', not 'vehicles').

4. When using "there exists... such that", carefully consider whether such contexts are guaranteed to exist in the context sequence. If uncertain, place the existential statement as the antecedent of an implication to provide protective conditions.

5. When expressing constraints involving thresholds that you are not sure about (a.k.a, fuzzy thresholds), use DESCRIPTIVE PHRASES (e.g., "within a certain range", "sufficiently high/low", "significantly higher/lower than", etc.) to describe them instead of specifying concrete values. These fuzzy thresholds will later be instantiated based on the context sequence.

6. For each context introduced by quantifiers, you can only access the fields defined in the <context_definitions> tag. Any derived concepts or properties must be computed using these fields from one or more contexts. Do not assume the existence of fields or properties that are not explicitly defined in the schema. So, for precisely expressing the semantics, consider how many contexts need to be introduced carefully.

7. Do not generate semantics that are already included in the existing constraints.

{% if few_shots %}
Here are some examples of semantics that you can refer to:
{% for shot in few_shots %}
- {{ shot.intent_and_semantics }}
{% endfor %}

Note: While these examples provide guidance, you should not limit yourself to similar patterns. Actively explore and utilize diverse sentence structures to express semantics. Your goal is to create practically meaningful, logically sound, and structurally varied constraint semantics that capture different aspects of the context sequence.
{% endif %}
"""

PHASE1_DUPLICATE_ERROR_PROMPT = """
The semantics you generated is duplicate or very similar to the existing constraints:
{{existing_semantics}}

Please generate a new intent and semantics, where the semantics is not duplicate or very similar to the existing constraints.
"""

# ---- Phase 2 Prompt ----
PHASE2_USER_PROMPT_TEMPLATE = """
The Phase 2 is to decompose the semantics into a structure and a list of bfunc signatures.

The structure is defined by the following grammar, which corresponds to common first-order logic constructs:
```lark
{{structure_grammar}}
```
Here are the key concepts to understand:
- "forall" corresponds to universal quantification ("for any...")
- "exists" corresponds to existential quantification ("there exists... such that")
- "implies" corresponds to logical implication ("if... then...")
- "and" corresponds to logical conjunction ("and")
- "or" corresponds to logical disjunction ("or")
- "not" corresponds to logical negation ("not")
- "bfunc" represents boolean expressions that will be defined in Phase 3

The list of bfunc signatures is declared using the `bfunc_signature` productions in the structure. Each bfunc signature consists of:
1. An ID number (starting from 1)
2. A list of parameters (variables) it operates on

Attention to the following points when you do converting:

1. Make sure the structure strictly follows the BNF grammar. (PAY ATTENTION TO PARENTHESIS!)

2. When converting the semantics into the structure, do not mechanically translate each part. Instead, carefully consider the global semantics and ensure that the resulting structure accurately captures the overall meaning and relationships expressed in the original semantics.

3. When decomposing the semantics into bfuncs, ensure that each bfunc's semantics can be computed using ONLY the contexts that have been introduced by quantifiers in the constraint structure. Do not create bfuncs that would require additional contexts beyond those already introduced.

4. When considering using "exists" quantifiers, carefully verify that such contexts are guaranteed to exist in the context sequence. If uncertain about existence, structure the formula so that existential quantification appears as the antecedent of an implication.

5. If you cannot decompose the semantics, you need to return an empty JSON object.

{% if few_shots %}
Here are the structures and lists of bfunc signatures that correspond to the semantics in previous examples:
{% for shot in few_shots %}
- {{ shot.structure_and_signatures }}
{% endfor %}
{% endif %}
"""

PHASE2_ROLLBACK_PROMPT_TEMPLATE = """
The structure and list of bfunc signatures you generated make it hard to implement bfunc bodies that match the semantics in Phase 3. 

Please regenerate the structure and list of bfunc signatures according to the specific reason below.

Reason: "{{rollback_reason}}"

Attention to the following points when you do regenerating:

1. Make sure the structure strictly follows the BNF grammar. (PAY ATTENTION TO PARENTHESIS!)

2. When decomposing the semantics into bfuncs, ensure that each bfunc's semantics can be computed using ONLY the contexts that have been introduced by quantifiers in the constraint structure. Do not create bfuncs that would require additional contexts beyond those already introduced.

3. When converting the semantics into the structure, do not mechanically translate each part. Instead, carefully consider the global semantics and ensure that the resulting structure accurately captures the overall meaning and relationships expressed in the original semantics.

4. When considering using "exists" quantifiers, carefully verify that such contexts are guaranteed to exist in the context sequence. If uncertain about existence, structure the formula so that existential quantification appears as the antecedent of an implication.

5. If you cannot regenerate the structure and list of bfunc signatures, you need to return an empty JSON object.
"""

PHASE2_SYNTAX_ERROR_PROMPT_TEMPLATE = """
The structure you generated has syntax errors. Please fix the errors according to the following error message, and return the fixed structure and list of bfunc signatures.

{{error_message}}

Attention to the following points when you do converting:

1. Make sure the structure strictly follows the BNF grammar. (PAY ATTENTION TO PARENTHESIS!)

2. When decomposing the semantics into bfuncs, ensure that each bfunc's semantics can be computed using ONLY the contexts that have been introduced by quantifiers in the constraint structure. Do not create bfuncs that would require additional contexts beyond those already introduced.

3. When converting the semantics into the structure, do not mechanically translate each part. Instead, carefully consider the global semantics and ensure that the resulting structure accurately captures the overall meaning and relationships expressed in the original semantics.

4. When considering using "exists" quantifiers, carefully verify that such contexts are guaranteed to exist in the context sequence. If uncertain about existence, structure the formula so that existential quantification appears as the antecedent of an implication.

5. If you cannot decompose the semantics, you need to return an empty JSON object.
"""

PHASE2_SEMANTIC_ERROR_PROMPT_TEMPLATE = """
Some bfunc signatures in the list you generated are invalid. Please fix the errors according to the following error message, and return the fixed structure and list of bfunc signatures.

{{error_message}}

Attention to the following points when you do converting:

1. Make sure the structure strictly follows the BNF grammar. (PAY ATTENTION TO PARENTHESIS!)

2. When decomposing the semantics into bfuncs, ensure that each bfunc's semantics can be computed using ONLY the contexts that have been introduced by quantifiers in the constraint structure. Do not create bfuncs that would require additional contexts beyond those already introduced.

3. When converting the semantics into the structure, do not mechanically translate each part. Instead, carefully consider the global semantics and ensure that the resulting structure accurately captures the overall meaning and relationships expressed in the original semantics.

4. When considering using "exists" quantifiers, carefully verify that such contexts are guaranteed to exist in the context sequence. If uncertain about existence, structure the formula so that existential quantification appears as the antecedent of an implication.

5. If you cannot decompose the semantics, you need to return an empty JSON object.
"""

# ---- Phase 3 Prompt ----
PHASE3_USER_PROMPT_TEMPLATE = """
The Phase 3 is to implement the body of every bfunc based on its signature. Each bfunc must evaluate to true or false based on its input parameters and should accurately reflect the constraint semantics.

The body of a bfunc is defined by the following grammar:
```lark
{{bg_logic_prods}}
```
In short, the body of a bfunc can be a single comparison expression or multiple expressions connected by '&&' (AND), '||' (OR), '->' (IMPLIES), and '!' (NOT).

A str_cmp_expr is defined by the following grammar:
```lark
{{bg_str_cmp_prods}}

{{bg_str_cmp_terminals}}
```
The `STR_SYMBOL NATURAL` (e.g., `STHRESHOLD1`) is to define a string symbol for a string fuzzy threshold that will be automatically instantiated later.

A num_cmp_expr is defined by the following grammar:
```lark
{{bg_num_cmp_prods}}

{{bg_num_cmp_terminals}}
```
The `NUM_SYMBOL NATURAL` (e.g., `NTHRESHOLD1`) is to define a numeric symbol for a numeric fuzzy threshold that will be automatically instantiated later.

Attention to the following points when you do implementing:

1. Make sure the body of a bfunc strictly follows the BNF grammar.

2. When accessing the fields of a context referenced by a parameter, you can only use the fields defined in the <context_definitions> tag. Any derived concepts or properties must be computed using these fields from one or more contexts (referenced by the parameters). Do not assume the existence of fields or properties that are not explicitly defined in the context schema.

3. Think carefully and deeply about how to implement the bfunc bodies. Make sure the implementation is rigorous and accurate.

4. {{response_prompt}}

{% if few_shots %}
Here are the bodies of bfuncs that correspond to the structures and lists of bfunc signatures in previous examples:
{% for shot in few_shots %}
- {{ shot.bfunc_implementations }}
{% endfor %}

Note: While these examples provide guidance, you should not limit yourself to similar patterns.
{% endif %}
"""

PHASE3_NO_SEMANTIC_CHECK_RESPONSE_PROMPT = """
If you cannot implement valid bfunc bodies, you need to return an empty JSON object.
"""

PHASE3_SEMANTIC_CHECK_RESPONSE_PROMPT = """
Your response format must follow these rules:
- If you can implement valid bfunc bodies, your response should only contain the "bodies" json field.
- If you cannot implement valid bfunc bodies, your response should only contain the "reason" field.

When you find it impossible to implement valid bfunc bodies (e.g., due to parameter count mismatch where implementing the bfunc body requires two parameters but only one is declared in its signature), you must provide a detailed `reason` explaining:
   - Which specific bfunc cannot be implemented
   - Why it cannot be implemented (specific technical limitations)
   - What modifications would be needed to make it implementable
   - **Consider whether the issue stems from unsafe existential quantification**: If the structure uses "exists" quantifiers in potentially unsafe positions (not as antecedents of implications), this may be causing implementation difficulties
"""

PHASE3_SEMANTIC_CHECK_FIELD_MUTUALLY_EXCLUSIVE_PROMPT = """
Your response is not valid! Field `reason` and field `bodies` are mutually exclusive, which means they cannot both be None or both be non-None. 

Your response format must follow these rules:
- If you can implement valid bfunc bodies, your response should only contain the "bodies" json field.
- If you cannot implement valid bfunc bodies, your response should only contain the "reason" field.

Please fix the errors, and return the fixed response.
"""

PHASE3_SYNTAX_ERROR_PROMPT_TEMPLATE = """
Some bfunc bodies in the list you implemented have syntax errors. Please fix the errors according to the following error message, and return the list of fixed bfunc bodies.

{{error_message}}

Attention to the following points when you do implementing:

1. Make sure the body of a bfunc strictly follows the BNF grammar.

2. When accessing the fields of a context referenced by a parameter, you can only use the fields defined in the <context_definitions> tag. Any derived concepts or properties must be computed using these fields from one or more contexts (referenced by the parameters). Do not assume the existence of fields or properties that are not explicitly defined in the context schema.

3. Think carefully and deeply about how to implement the bfunc bodies. Make sure the implementation is rigorous and accurate.

4. {{response_prompt}}
"""

PHASE3_CONSISTENCY_ERROR_PROMPT_TEMPLATE = """
Some bfunc bodies in the list you implemented are not consistent with their corresponding bfunc signatures. Please fix the errors according to the following error message, and return the list of fixed bfunc bodies.

{{error_message}}

Attention to the following points when you do implementing:

1. Make sure the body of a bfunc strictly follows the BNF grammar.

2. When accessing the fields of a context referenced by a parameter, you can only use the fields defined in the <context_definitions> tag. Any derived concepts or properties must be computed using these fields from one or more contexts (referenced by the parameters). Do not assume the existence of fields or properties that are not explicitly defined in the context schema.

3. Think carefully and deeply about how to implement the bfunc bodies. Make sure the implementation is rigorous and accurate.

4. {{response_prompt}}
"""

PHASE3_QUERY_UNIT_PROMPT_TEMPLATE = """
To further ensure the correctness of bfunc bodies, you need to analyze the units of the given constants (enclosed in <constants> tags) and symbols (enclosed in <symbols> tags) in the given expression (enclosed in <expression> tags).

<constants>
{{constants}}
</constants>

<symbols>
{{symbols}}
</symbols>

<expression>
semantics: {{semantics}}
implementation: {{implementation}}
</expression>

IMPORTANT NOTES:
1. The constants and symbols are both collected from left to right in the given expression.

2. The name of unit should be acceptable by pint package.

3. The order of constants and symbols in your response must strictly follow the order provided in the <constants> and <symbols> tags above.
"""

PHASE3_UNIT_ERROR_PROMPT_TEMPLATE = """
Some bfunc bodies in the list you implemented have semantic errors. Please fix the errors according to the following error message, and return the list of fixed bfunc bodies.

{{error_message}}

Attention to the following points when you do implementing:

1. Make sure the body of a bfunc strictly follows the BNF grammar.

2. When accessing the fields of a context referenced by a parameter, you can only use the fields defined in the <context_definitions> tag. Any derived concepts or properties must be computed using these fields from one or more contexts (referenced by the parameters). Do not assume the existence of fields or properties that are not explicitly defined in the context schema.

3. Think carefully and deeply about how to implement the bfunc bodies. Make sure the implementation is rigorous and accurate.

4. {{response_prompt}}
"""

# ---- Phase 4 Prompt ----

PHASE4_ADD_RESTRICTIONS_PROMPT_TEMPLATE = """
To facilitate the instantiation of fuzzy thresholds, you need to add restrictions for the following symbols in the bfuncs:

{% for bfunc_id, bfunc_info in restrict_bfunc_symbol_dict.items() %}
**{{ bfunc_id }}**:
- Semantics: {{ bfunc_info.semantics }}
- Implementation: {{ bfunc_info.implementation }}
- Symbols: {{ bfunc_info.symbols | join(', ') }}

{% endfor %}

A restriction for a symbol is an expression that restricts the symbol to a specific range or value. The restriction expression is defined by the following grammar:
```lark
{{restriction_grammar}}
```
The grammar supports range and value restrictions for numeric symbols, and value restrictions for string symbols.

**Follow these 3 steps to generate restrictions for each symbol:**

**Step 1: Determine bound type from implementation**
- Carefully analyze the comparison operator associated with the symbol in the bfunc implementation (e.g., `>`, `<`, `>=`, `<=`, `==`, `!=`)
- If symbol appears on the right side of `> symbol` or `>= symbol`, the symbol represents a lower bound
- If symbol appears on the right side of `< symbol` or `<= symbol`, the symbol represents an upper bound
- If symbol appears in `== symbol` or `!= symbol`, the symbol represents a specific value

**Step 2: Determine degree from semantics**
- Extract degree information from the bfunc semantics (direction is already determined by Step 1). Examples of degree keywords:
   - "significant", "obvious", "substantial" and similar words → large degree
   - "close", "similar", "near" and similar words → small degree
   - "sufficient", "adequate" and similar words → moderate degree
   - "far exceeds", "far below" and similar words → extreme degree
   - "slightly higher", "slightly lower" and similar words → minor degree

**Step 3: Determine physical meaning from context**
- Based on the bfunc semantics, identify the physical meaning and reasonable numerical range. Examples include:
   - Speed-related: Consider realistic traffic speeds
   - Distance-related: Consider typical trip distances
   - Time-related: Consider realistic time intervals
   - Ratio-related: Consider meaningful percentages
   - Count-related: Consider reasonable quantities
   - And similar physical concepts with their corresponding realistic ranges

**Apply the above steps to generate restrictions:**
- Use Step 1 to determine the restriction type (upper bound, lower bound, or specific value)
- Use Step 2 to determine the degree magnitude (how strict/loose the restriction should be)
- Use Step 3 to determine the appropriate numerical range based on physical meaning
- Only define ONE restriction for each symbol
- Ensure the restriction follows grammar rules and has practical meaning

If you cannot define restriction for some symbols, you can skip them and define restrictions for the others.

{% if few_shots %}
Here are the restrictions that correspond to the bfunc bodies in previous examples, you should review previous examples to better understand how to define restrictions:
{% for shot in few_shots %}
- {{ shot.restrictions }}
{% endfor %}
{% endif %}
"""

PHASE4_FIX_RESTRICTION_SYNTAX_ERROR_PROMPT_TEMPLATE = """
Some restrictions in the list you defined have syntax errors. Please fix the errors according to the following error message, and return the list of fixed restrictions.

{{error_message}}

**Follow these 3 steps to generate restrictions for each symbol:**

**Step 1: Determine bound type from implementation**
- Carefully analyze the comparison operator associated with the symbol in the bfunc implementation (e.g., `>`, `<`, `>=`, `<=`, `==`, `!=`)
- If symbol appears on the right side of `> symbol` or `>= symbol`, the symbol represents a **lower bound**
- If symbol appears on the right side of `< symbol` or `<= symbol`, the symbol represents an **upper bound**
- If symbol appears in `== symbol` or `!= symbol`, the symbol represents a **specific value**

**Step 2: Determine degree from semantics**
- Extract degree information from the bfunc semantics (direction is already determined by Step 1). Examples of degree keywords:
   - "significant", "obvious", "substantial" and similar words → large degree
   - "close", "similar", "near" and similar words → small degree
   - "sufficient", "adequate" and similar words → moderate degree
   - "far exceeds", "far below" and similar words → extreme degree
   - "slightly higher", "slightly lower" and similar words → minor degree

**Step 3: Determine physical meaning from context**
- Based on the bfunc semantics, identify the physical meaning and reasonable numerical range. Examples include:
   - Speed-related: Consider realistic traffic speeds
   - Distance-related: Consider typical trip distances
   - Time-related: Consider realistic time intervals
   - Ratio-related: Consider meaningful percentages
   - Count-related: Consider reasonable quantities
   - And similar physical concepts with their corresponding realistic ranges

**Apply the above steps to generate restrictions:**
- Use Step 1 to determine the restriction type (upper bound, lower bound, or specific value)
- Use Step 2 to determine the degree magnitude (how strict/loose the restriction should be)
- Use Step 3 to determine the appropriate numerical range based on physical meaning
- Only define ONE restriction for each symbol
- Ensure the restriction follows grammar rules and has practical meaning

If you cannot define restriction for some symbols, you can skip them and define restrictions for the others.
"""
