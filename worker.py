import requests
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

# ---- Watsonx LLM setup ----
PROJECT_ID = "skills-network"
credentials = {
    "url": "https://us-south.ml.cloud.ibm.com"
    # "apikey": "Your WatsonX API"  # Not needed in Cloud IDE
}
model_id = "mistralai/mistral-medium-2505"
parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.MAX_NEW_TOKENS: 1024
}
model = Model(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=PROJECT_ID
)

# ---- Watsonx text processing ----
def watsonx_process_message(user_message):
    prompt = f"""
    Translate the following English sentence into Spanish. 
    Reply ONLY with the translation, no explanations, no formatting, no extra text.
    English: {user_message}
    Spanish:
    """
    response_text = model.generate_text(prompt=prompt)
    print("watsonx response:", response_text)
    return response_text.strip()

# ---- Watson Speech-to-Text ----
def speech_to_text(audio_binary):
    base_url = 'https://sn-watson-stt.labs.skills.network'
    api_url = base_url + '/speech-to-text/api/v1/recognize'
    params = {'model': 'en-US_Multimedia'}
    response = requests.post(api_url, params=params, data=audio_binary).json()
    text = 'null'
    if bool(response.get('results')):
        print('Speech-to-Text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('Recognized text:', text)
    return text

# ---- Watson Text-to-Speech ----
def text_to_speech(text, voice=""):
    base_url = 'https://sn-watson-tts.labs.skills.network'
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }
    json_data = {'text': text}
    response = requests.post(api_url, headers=headers, json=json_data)
    print('Text-to-Speech response:', response)
    return response.content

