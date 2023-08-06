import requests
import json

class GPT3(object):
    def __init__(self, endpoint_url, api_key, model):
        self.api_key = api_key
        self.endpoint_url = endpoint_url
        self.model = model

    def __call__(self, prompt, num_responses=1, topk=0, presence_penalty=0, max_tokens=1):
        if not isinstance(prompt, list):
            prompt = [prompt]
        prompt = [p.replace("'", "").replace('"', "") for p in prompt]
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.9,
            "n": num_responses,
            "stream": False,
            "logprobs": topk,
            "presence_penalty": presence_penalty,
            "stop": ["<|endoftext|>", "\\n"]
        }
        r = requests.post(self.endpoint_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json = payload
        )      
        output = json.loads(r.content)
        return output

    def from_prompt(self, prompt, topk=10, max_tokens=10):
        output = self.__call__(prompt, topk=topk, max_tokens=max_tokens)
        return output["choices"][0]["text"]