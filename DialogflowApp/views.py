from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import dialogflow
import os
import json	
# Create your views here.

def dialogflowui(request):
	# return render(request,)
	return HttpResponse(" Done Done Done")

def convert(data):
    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return map(convert, data)

    return data


@csrf_exempt
# @require_http_methods(['POST'])
def chat_view(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        GOOGLE_AUTHENTICATION_FILE_NAME = "travelinowhatsappbot-pplcjc-7d0421d8d901.json"
        current_directory = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(current_directory, GOOGLE_AUTHENTICATION_FILE_NAME)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
        GOOGLE_PROJECT_ID = "travelinowhatsappbot-pplcjc"
        session_id = "1234567891"
        context_short_name = "does_not_matter"
        context_name = "projects/" + GOOGLE_PROJECT_ID + "/agent/sessions/" + session_id + "/contexts/" + context_short_name.lower()
        parameters = dialogflow.types.struct_pb2.Struct()
        context_1 = dialogflow.types.context_pb2.Context(name=context_name,lifespan_count=2,parameters=parameters)
        query_params_1 = {"contexts": [context_1]}
        language_code = 'en'
        response = detect_intent_with_parameters(project_id=GOOGLE_PROJECT_ID,session_id=session_id,query_params=query_params_1,language_code=language_code,user_input=message)
        a = response.query_result.fulfillment_text
        return JsonResponse({'Result':a})
    else:
        return JsonResponse({'Result': "Invalid request"})


def detect_intent_with_parameters(project_id, session_id, query_params, language_code, user_input):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    #text = "this is as test"
    text = user_input

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input,
        query_params=query_params
    )

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))
    return response