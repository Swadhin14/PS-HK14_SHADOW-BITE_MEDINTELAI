from services.llm_service import generate_response

prompt = "Explain diabetes in simple terms."

output = generate_response(prompt)

print(output)