import requests
import json

def emotion_detector(text_to_analyze):
    # Define the URL and headers for the Watson Emotion Predict function
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    

    if not text_to_analyze.strip():  # Check for blank or empty input
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
        
    # Create the input JSON payload
    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    # Send the POST request to the Watson NLP service
    response = requests.post(url, headers=headers, json=payload)
    
     # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        response_json = response.json()
        
        # Extract the first emotion prediction (if exists)
        if 'emotionPredictions' in response_json and len(response_json['emotionPredictions']) > 0:
            emotions = response_json['emotionPredictions'][0]['emotion']
            
            # Extract the required emotions
            anger_score = emotions.get('anger', 0)
            disgust_score = emotions.get('disgust', 0)
            fear_score = emotions.get('fear', 0)
            joy_score = emotions.get('joy', 0)
            sadness_score = emotions.get('sadness', 0)
            
            # Find the dominant emotion
            emotion_scores = {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score
            }
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            
            # Return the formatted dictionary
            return {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score,
                'dominant_emotion': dominant_emotion
            }
        else:
            return "No emotion predictions found in the response."
    else:
        # Handle error if request was not successful
        return f"Error: {response.status_code} - {response.text}"