from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from streamapp.webcamera import YzatCamera
# Create your views here.

def index(request):
	return render(request, 'myface/home.html')

def gen(camera):
	while True:
		frame = webcamera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
	return StreamingHttpResponse(gen(YzatCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')


