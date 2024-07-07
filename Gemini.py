"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os

import google.generativeai as genai

 
genai.configure(api_key="AIzaSyCTFL4ungMwhqj84sKSCsLVvsm47PCEOxM")

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)


def get_response_from_gemini(user_input):
    # Make the request to the Gemini API with the user input
    response = model.generate_content([
      {"text": f"input: {user_input}"},
      {"text": "output: "}
    ])
    
    # Assuming the response has a text attribute with the result
    # Adjust based on the actual structure of the response
    if response is not None and hasattr(response, 'text'):
        return response.text
    else:
        return "Response is empty or not valid."
response_text = get_response_from_gemini(input)
print(response_text)




