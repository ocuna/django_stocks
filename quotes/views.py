from django.shortcuts import render, redirect
from . models import Stock
from . forms import StockForm
from django.contrib import messages

import requests
import json
import topsecret

def home(request):

	iexcloud_TPK = topsecret.keys['iexcloud_TPK']
	stock_code = ''
	api = ''
	api_error = ''

	if request.method == "POST":
		stock_code = request.POST['stock_code']
		sandbox_string = "https://sandbox-sse.iexapis.com/stable/stock/" + stock_code + "/quote?types=quotes&symbols=spy&format=json&token=" + iexcloud_TPK
		api_request = requests.get(sandbox_string)


		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api_error = "The Stock Code: <i>" +  stock_code  + "</i> returned no matches.  Please try again."

	else:
		api_error = "Error...Please enter a Stock Code for your quote."


	context = {
		'api': api,
		'api_error': api_error,
	}

	return render(request, 'home.html', context)



def about(request):
	return render(request, 'about.html', {})
 	
def add_stock(request):

	if request.method == "POST":
		modify_post = request.POST.copy()
		modify_post['ticker'] = modify_post['ticker'].upper() 
		form = StockForm(modify_post or None)
		stock_code = request.POST['ticker']

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock code: <i>" + stock_code + "</i> has been added"))
			return redirect('add_stock')

	else:
		ticker_codes = Stock.objects.all().order_by('ticker')
		# assert False, ticker_codes

		# there maybe no codes to lookup
		if ticker_codes != None:
			# setup all or vars:
			iexcloud_PK = topsecret.keys['iexcloud_PK']
			iexcloud_TPK = topsecret.keys['iexcloud_TPK']
			stock_code = ''
			api = ''
			api_error = ''
			code_string = ''
			consume_api = []

			# if the query worked, we have to iterate it to get the codes out
			for code in ticker_codes:
				code_string = code_string + ',' + code.ticker

			# remove the first comma
			code_string = code_string[1:]

			batch_sandbox_string = "https://sandbox-sse.iexapis.com/stable/stock/market/batch?symbols="+ code_string.lower() +"&types=quote&format=json&token=" + iexcloud_TPK
			api_request = requests.get(batch_sandbox_string)


			try:
				api = json.loads(api_request.content)
				for ticker,value in api.items():
					consume_api.append(api[ticker]['quote'])
				assert False, consume_api
			except Exception as e:
				api_error = "The Stock Code(s): <i>" +  code_string.upper()  + "</i> returned no matches.  Please try again."
			else:
				api_error = "Error...the API connection with the server has failed, Please contact the webmaster@thiswebsite.com"


		context = {
			'api': consume_api,
			'api_error': api_error,
			'ticker_codes': ticker_codes,
		}
		return render(request, 'add_stock.html', context)

def delete_stock(request, stock_id):
	stock = Stock.objects.get(pk = stock_id)
	stock_code = stock.ticker
	stock.delete()
	messages.success(request, ("Stock code: <i>" + stock_code + "</i> has been deleted"))
	return redirect('add_stock')