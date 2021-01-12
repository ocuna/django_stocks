from django.shortcuts import render

def home(request):
	import requests
	import json
	import secret

	api_request = requests.get("https://cloud-sse.iexapis.com/stable/appl?token=pk_b6c1244719c34382af76899765d33a3e&symbols=spy")

	pk = secret.secrets['iexcloud_PK']


	context = {
		'pk':pk,
	}

	return render(request, 'home.html', context)



def about(request):
	return render(request, 'about.html', {})
 	