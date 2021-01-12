from django.shortcuts import render
import requests
import json
import topsecret

def home(request):

	iexcloud_PK = topsecret.keys['iexcloud_PK']
	iexcloud_TPK = topsecret.keys['iexcloud_TPK']
	stock_code = ''

	if request.method == "POST":
		stock_code = request.POST['stock_code']

	sandbox_string = "https://sandbox-sse.iexapis.com/stable/stock/" + stock_code + "/quote?types=quotes&symbols=spy&format=json&token=" + iexcloud_TPK
	request_string = "https://cloud-sse.iexapis.com/stable/" + stock_code + "/batch?types=quotes&token=" + iexcloud_PK
	api_request = requests.get(sandbox_string)


	try:
		api = json.loads(api_request.content)
		api_error = ""
	except Exception as e:
		api = sandbox_string
		api_error = "Error..."



	context = {
		'api': api,
		'api_error': api_error,
	}

	return render(request, 'home.html', context)



def about(request):
	return render(request, 'about.html', {})
 	
 	#https://sandbox-sse.iexapis.com/stable/stock/appl/quote?types=quotes&symbols=spy&format=json&token=Tpk_ccc874f4472b439eba7d27315ba4145c
 	#https://sandbox-sse.iexapis.com/stable/stock/aapl/quote?types=quotes&symbols=spy&format=json&token=Tpk_ccc874f4472b439eba7d27315ba4145c