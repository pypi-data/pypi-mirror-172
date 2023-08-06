from urllib.parse import urljoin
import requests_html

session = requests_html.HTMLSession()

class Librus():
    #login
    def login(login, haslo):
        session.get(url="https://api.librus.pl/OAuth/Authorization?client_id=46&response_type=code&scope=mydata")
        r = session.post(url="https://api.librus.pl/OAuth/Authorization?client_id=46", data={'action': 'login', 'login': login, 'pass': haslo})

        try:
            session.get(url=urljoin(r.url, r.json()["goTo"]))
        except:
            print("Podano zły login lub hasło.")


    #szczęśliwy numerek
    def szczesliwy_numerek():
        r = session.get(url="https://synergia.librus.pl/uczen/index")
        return r.html.find("span.luckyNumber")[0].text


    #informacje
    class informacje():
        def uczen():
            r = session.get(url="https://synergia.librus.pl/informacja")
            return r.html.xpath('/html/body/div[3]/div[3]/div/div/table/tbody/tr[1]/td')[0].text
        def klasa():
            r = session.get(url="https://synergia.librus.pl/informacja")
            return r.html.xpath('/html/body/div[3]/div[3]/div/div/table/tbody/tr[2]/td')[0].text
        def numer_w_dzienniku():
            r = session.get(url="https://synergia.librus.pl/informacja")
            return r.html.xpath('/html/body/div[3]/div[3]/div/div/table/tbody/tr[3]/td')[0].text
        def wychowawca():
            r = session.get(url="https://synergia.librus.pl/informacja")
            return r.html.xpath('/html/body/div[3]/div[3]/div/div/table/tbody/tr[4]/td')[0].text