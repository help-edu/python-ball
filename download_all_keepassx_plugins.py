import re
import requests



page = 'http://keepass.info'
print ('opening a', page)

r =  requests.get(page + '/plugins.html')

print('status code is ', r.status_code)

if r.status_code is 200:
	result = re.findall('"[^"]+\.zip', r.text)
	
	print('amount of plugins ', len(result))

	for lnk in result:
		lnk = lnk[1:]
		filename = re.findall( '[^/]+', lnk[::1])[-1:][0];

		if lnk.startswith( 'http' ) is False:
			lnk = page + '/' + lnk

		print('Downloading from ', lnk, ' ', end = "")
		while True:
			try:
				lnk_r = requests.get(lnk)
			except:
				print('.', end="")
				continue

			if lnk_r.status_code is 200:
				with open(filename, 'wb') as f:
					f.write(lnk_r.content)

				print("(OK)")
			else:
				print("ERROR!")

			break


	print(result)

