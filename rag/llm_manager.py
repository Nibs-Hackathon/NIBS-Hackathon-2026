import os
from langchain_google_genai import ChatGoogleGenerativeAI


class LLMManager:


    def __init__(self):

        self.keys = [
            os.getenv("GEMINI_KEY_1"),
        ]

        self.current = 0


    def get_model(self):

        key = self.keys[self.current]

        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=key,
            temperature=0.2
        )


    def generate(self, prompt):

        attempts = len(self.keys)

        while attempts > 0:

            try:

                model = self.get_model()

                response = model.invoke(prompt)

                return response.content


            except Exception as e:

                print(
                    f"LLM key {self.current+1} failed:",
                    e
                )


                self.current += 1

                if self.current >= len(self.keys):
                    self.current = 0


                attempts -= 1


        return "All LLM providers unavailable."