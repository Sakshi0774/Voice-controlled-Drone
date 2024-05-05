import requests
import time


# from api_secrets import api_key
# import sys

# Four steps involved:
# 1) Upload the audio file to assemblyai
# 2) Transcription
# 3) Polling the API
# 4) Save the transcript

# Upload
def convert_to_text():
    api_key = "7966e3744df54083922a7bf60ee3c65c"
    filename = "output.wav"
    upload_endpoint = 'https://api.assemblyai.com/v2/upload'
    transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

    headers_auth_only = {'authorization': api_key}

    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }

    def upload(filename):
        def read_file(filename, chunk_size=5242880):
            with open(filename, 'rb') as _file:
                while True:
                    data = _file.read(chunk_size)
                    if not data:
                        break
                    yield data

        upload_response = requests.post(upload_endpoint, headers=headers_auth_only, data=read_file(filename))

        audio_url = upload_response.json()['upload_url']
        return audio_url

    # transcribe
    def transcribe(audio_url):
        transcript_request = {"audio_url": audio_url}
        response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
        job_id = response.json()['id']
        return job_id

    # poll
    def poll(transcript_id):
        polling_endpoint = transcript_endpoint + '/' + transcript_id
        polling_response = requests.get(polling_endpoint, headers=headers)
        return polling_response.json()

    def get_transcription_result_url(audio_url):
        transcript_id = transcribe(audio_url)
        while True:
            data = poll(transcript_id)
            print("Received data:", data)  # Add this line for debugging
            if 'status' in data and data['status'] == 'completed':
                return data, None
            elif 'status' in data and data['status'] == 'error':
                return data, data.get('error')
            time.sleep(1)

    def save_transcript(audio_url):
        data, error = get_transcription_result_url(audio_url)

        if data:
            txt_filename = filename + ".txt"
            with open(txt_filename, "w") as f:
                f.write(data['text'])
            print("Transcription saved!")
        elif error:
            print("Error!", error)

    # upload
    audio_url = upload(filename)
    save_transcript(audio_url)
