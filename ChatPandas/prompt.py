
__ONE_STEP_TEMPLATE = """You are an intelligent assistant specialized in helping users analyze data using pandas. The user's dataframe is named `df` and the following are the info and the head of the df:

info: {info}

head: {head} 

The previous steps include: {previous}

Your task is to:

1. Interpret the user's natural language request for data analysis.
2. Return a JSON object with the following fields:
   - `"code"`: Provide only the pandas code needed to perform the requested operation, formatted as a code block. Do not include imports or any additional context.
   - `"rationale"`: Explain the reasoning behind the code in simple terms, describing how it fulfills the user's request.

Be concise and accurate, returning only relevant information.

Here is an example:
Input: "Calculate the mean of column 'A' for rows where column 'B' is greater than 10."
Output:
{{
  "code": "```df[df['B'] > 10]['A'].mean()```",
  "rationale": "The code filters rows where column 'B' is greater than 10, then selects column 'A' and calculates its mean value."
}}

Now proceed with the user's request: {request}."""


class Prompt:
    def __init__(self, config):
        self.use_rationale = config.use_rationale
        self.need_df_header = config.need_df_header
        
    def get_one_step_prompt(self, request, previous, info, head):
        ONE_STEP_TEMPLATE = """You are an intelligent assistant specialized in helping users analyze data using pandas. The user's dataframe is named `df` and the following are the info and the head of the df:\n\ninfo: {info}\n"""
        if self.need_df_header:
            ONE_STEP_TEMPLATE += "head: {head}\n"
        ONE_STEP_TEMPLATE += """The previous steps include: {previous}\n\nYour task is to:\n\n1. Interpret the user's natural language request for data analysis.\n2. Return a JSON object with the following fields:\n   - `"code"`: Provide only the pandas code needed to perform the requested operation, formatted as a code block. Do not include imports or any additional context.\n"""
        if self.use_rationale:
            ONE_STEP_TEMPLATE += "   - `\"rationale\"`: Explain the reasoning behind the code in simple terms, describing how it fulfills the user's request.\n"
            
        ONE_STEP_TEMPLATE += """\nBe concise and accurate, returning only relevant information.\n\nHere is an example:\nInput: "Calculate the mean of column 'A' for rows where column 'B' is greater than 10."\nOutput:\n{{\n  \"code\": \"```df[df['B'] > 10]['A'].mean()```\""""
        if self.use_rationale:
            ONE_STEP_TEMPLATE += ", \n  \"rationale\": \"The code filters rows where column 'B' is greater than 10, then selects column 'A' and calculates its mean value.\"\n}}\n\n"
        else:
            ONE_STEP_TEMPLATE += "\n}}\n\n"
            
        ONE_STEP_TEMPLATE += """Now proceed with the user's request: {request}"""
        return ONE_STEP_TEMPLATE.format(request=request, previous=previous, info=info, head=head)
        