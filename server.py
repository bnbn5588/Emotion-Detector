"""Module providing a function printing python version."""

from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detection():
    """
    Handle POST requests to analyze emotions from the provided text.

    This function accepts JSON data containing a 'text' field, 
    runs the emotion detection on the provided text, and returns 
    the results in a formatted response.

    Returns:
        A JSON response containing emotion scores or an error message.
    """
    data = request.json
    text_to_analyze = data.get('text')

    if not text_to_analyze:
        return jsonify({'error': 'No text provided'}), 400

    result = emotion_detector(text_to_analyze)
    dominant_emotion = result['dominant_emotion']

    if dominant_emotion is None:
        return jsonify({'error': 'Invalid text! Please try again.'}), 400

    # Format the response as required
    response = (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
        f"'joy': {result['joy']} and 'sadness': {result['sadness']}. "
        f"The dominant emotion is {dominant_emotion}."
    )

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
