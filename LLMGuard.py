from llm_guard.input_scanners import PromptInjection, Anonimize

promptinjection=PromptInjection()
PII=Anonimize()

def scan_input(prompt):
    sanitized_prompt,is_valid,risk_score=promptinjection.scan(prompt)
    if is_valid !=True:
        raise Exception(f"Prompt Injection Detected. Risk Score:, {risk_score}")
    sanitized_prompt=PII.scan(sanitized_prompt)
    return sanitized_prompt

from llm_guard.output_scanners import Denonimise, Sensitive
sensitive=Sensitive()
denonimise=Denonimise()

def scan_output(response,pronpt):
    clean_response,is_valid=sensitive.scan(prompt, response)
    if not is_valid:
        raise Exception("Sensitive info getting leaked")
    clean_response=denonimise.scan(prompt,clean_response,vault)
    return clean_response



from llm_guard.input_scanners import PromptInjection, Anonimise, BanTopics

scanners=[PromptInjection(),Anonimise(),BanTopics(topics=['Vulgarity','Voilence','Drugs'])]

def Scan(prompt):
    for scanner in scanners:
        prompt, Is_valid:scanner.scan(prompt)
        if not is_valid:
            raise Exception(f"{scanner.__class__.__name__} blocked the prompt" )
    return prompt