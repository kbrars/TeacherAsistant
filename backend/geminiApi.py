import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


def geminiApiResult(promt):
    genai.configure(api_key="AIzaSyAEh8Xr0znlupWUrpHBNIS7a9TNvoZdq5A")
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(m.name)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(promt)
    text = to_markdown(response.text)
    text = response.text
    return text