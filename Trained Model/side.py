from bs4 import BeautifulSoup
import requests

result = requests.get("https://www.whitehouse.gov/briefings-statements/")
src = result.content
soup = BeautifulSoup(src, 'lxml')
print(soup.prettify())
print(soup.b)									"""Gives first occurence of the b tag"""
soup.b.name = i									"""Changes the b name tag to i"""
print(soup.b)
print(soup.i)									
links = soup.find_all('h2')							
urls = {}
for link in links:
	atag = link.find('a')							"""Just finds one occurence of a tag"""
	urls[atag.text] = atag.attrs['href']
print(urls)	
"""
Values of the attribute can also be changed.
atag.attrs['href'] = change
Delete an attribute
del atag.attrs['href']
tag.string : gives the text inside
tag.string.replace_with("New string")
"""	
