import os
import dialogflow_v2
from google.api_core.exceptions import InvalidArgument

def chatbot(text_to_be_analyzed):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'rai_modules/rai_voniq/private_key.json' # หาenvironment ชื่อ Google app credentials แล้ว add new environmental variable named private_key
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:\\Users\\ThanaphatJ\\Desktop\\Django\\voniq\\voice_assist\\app1\\private_key.json' # หาenvironment ชื่อ Google app credentials แล้ว add new environmental variable named private_key

    DIALOGFLOW_PROJECT_ID = 'smartlab-dbmvqk'
    DIALOGFLOW_LANGUAGE_CODE = 'en'
    SESSION_ID = 'me'

    session_client = dialogflow_v2.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow_v2.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow_v2.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise Exception("Sorry")

    # print("Query text:", response.query_result.query_text)
    # print("Detected intent:", response.query_result.intent.display_name)
    # print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    # print("Fulfillment text:", response.query_result.fulfillment_text)
    return response.query_result.fulfillment_text