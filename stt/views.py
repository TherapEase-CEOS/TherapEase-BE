from django.shortcuts import render
from django.http import HttpResponse
import speech_recognition as sr

def speech_to_text(request):
    recognizer = sr.Recognizer()

    # 마이크로폰에서 음성 녹음
    with sr.Microphone() as source:
        print("무언가 말해보세요...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ko-KR")
        return HttpResponse(f"당신이 말한 내용: {text}")
    except sr.UnknownValueError:
        return HttpResponse("죄송합니다, 음성을 이해하지 못했습니다.")
    except sr.RequestError as e:
        return HttpResponse(f"요청 오류: {e}")

