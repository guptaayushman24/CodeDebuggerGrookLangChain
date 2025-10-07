import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fastapi import FastAPI
from pydantic import BaseModel
from langserve import add_routes
from langchain_core.output_parsers import StrOutputParser
import uvicorn
import re
class QueryRequest (BaseModel) :
    language:str
    code :str
try :
    groq_api_key = os.getenv("GROQ_API_KEY")
    model = ChatGroq(model="llama-3.1-8b-instant",groq_api_key=groq_api_key)
    generic_template = """
    You are a {language} syntax checker.
Check the following code for **syntax errors** and potential **runtime errors**.
Suggest corrections only for errors found.
Explain each error clearly, then provide the corrected code in a fenced code block.
Use the following format:

Errors:  
1. <Error explanation>

Corrected Code:
```{language}
<corrected code>
"""


    parser = StrOutputParser()
    prompt=ChatPromptTemplate.from_messages([
       ("system",generic_template),
       ("user","{code}")
    ])
    chain = prompt|model|parser

    app=FastAPI(
        title="LangChain Server",
        version="1.0",
        description="Code Debug"
    )
    add_routes(
        app,
        chain,
        path='/chain'
    )
    

    @app.post("/debugcode")
    def check_syntax_of_code (request:QueryRequest) :
        language =  request.language
        code = request.code

        

        result = chain.invoke({"language":language,"code":code})
        errors_match = re.search(r"Errors:\s*(.*?)\n\nCorrected Code:", result, re.DOTALL)
        errors_list = []
        if errors_match:
            errors_text = errors_match.group(1)
            # Split numbered list
            errors_list = [line.split(". ",1)[1].strip() for line in errors_text.strip().split("\n") if line.strip()]

        # Extract corrected code
        code_match = re.search(r"Corrected Code:\n```[A-Za-z]*\n(.*?)```", result, re.DOTALL)
        corrected_code = code_match.group(1).strip() if code_match else ""

        return {
            "errors": errors_list,
            "corrected_code": corrected_code
        }

    
        

    if __name__=="__main__" :
     uvicorn.run(app,host="0.0.0.0",port=8000)
except RuntimeError as e:
    print(e)
