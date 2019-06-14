from bs4 import BeautifulSoup
import requests

result = requests.get("https://www.google.com/");	"""Lets you access the webpage"""

print(result.status_code)	"""HTTP status code(200:content present, 404:content missing)"""
print(result.headers)					"""Print out headers of the page"""
src = result.content
soup = BeautifulSoup(src, 'lxml');			"""To create an object of class BeautifulSoup"""
links = soup.find_all("a")				"""finds all the a tags"""
for link in links:
	if "About" in link.text:			"""Searching for text in between the tags"""
		print(link.attrs['href'])		"""Displaying the attribute href from the tag"""
print(result)
