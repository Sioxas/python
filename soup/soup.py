from bs4 import BeautifulSoup

r = "<div>afadfasfds<br/>asdadfsdf<br/><br/>asdfdfsdf<br/></div>"
soup = BeautifulSoup(r, "html.parser")
innerHtml = soup.div.get_text()
print(innerHtml)
