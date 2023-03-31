BASE_PROMT = \
"""I want you to act as an AI assistant answer the request based on the context below (it could be empty).
Your knowledge cutoff is 2021-09, and the current date is 2023-03-30.
My name is Igor.

EXAMPLE
Request: I live in Russia and have no visa in any country that requires a visa for Russian citizens. What is the usual weather in Siberia in April?

Previous observations:
The user has mentioned that they do not like cold weather but enjoy warm weather and beaches.

Answer: The weather in Siberia in April can vary depending on the specific location within Siberia.

END OF EXAMPLE\n"""


def get_promt(query: str, context: str) -> str:
    return BASE_PROMT + \
        f"Request: {query}\n" + \
        f"Previous observations: {context}\n" + \
        f"Answer:"

SUMMARY_PROMT = \
"""My name is {}. 
I want to ask you the following question:
{}
Do not answer it, but please summarise what did you learn about me?
In answer, use my name instead of a personal pronoun. Ise past tenses."""
