import os
import time
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.inference.ai.azure.com"
model_name = "Phi-4"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

def benchmark_model():
    messages = [
        UserMessage("what it is 5s in mechanical eng.?"),
        UserMessage("WHat it is first law of thermodynamics?"),
        UserMessage("How machine learning works? explain in 2 lines maximum"),
        UserMessage("Como funciona uma classe em machine learning?")
    ]

    for message in messages:
        start_time = time.time()
        response = client.complete(
            messages=[message],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Message: {message.content}")
        print(f"Response: {response.choices[0].message.content}")
        print(f"Time taken: {elapsed_time:.2f} seconds\n")

if __name__ == "__main__":
    benchmark_model()