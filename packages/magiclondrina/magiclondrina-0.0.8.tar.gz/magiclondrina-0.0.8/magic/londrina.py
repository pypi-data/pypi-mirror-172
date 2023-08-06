from bs4 import BeautifulSoup
import requests as re
from tabulate import tabulate
import scrython


def get_info(card_name):
    print("Pesquisando carta na base de dados...")
    try:
        card = scrython.cards.Named(fuzzy=card_name)
        card_name = str(card.name())
    except scrython.foundation.ScryfallError:
        print("Carta não encontrada. ")
        return None

    url = "https://mypcards.com/Piedade/magic?PastaSearch%5BexibirSomenteVenda%5D=0&PastaSearch" \
            "%5BexibirSomenteVenda%5D=1&PastaSearch%5Bquery%5D=" + f"{card_name.replace(' ', '+').strip()}" + "&" \
            "PastaSearch%5BexibirSomenteDesejos%5D=0&PastaSearch%5BquantidadeRegistro%5D=20"

    url_wlad = "https://mypcards.com/Wlad/magic?PastaSearch%5BexibirSomenteVenda%5D=0&PastaSearch" \
                "%5BexibirSomenteVenda%5D=1&PastaSearch%5Bquery%5D=" + f"{card_name.replace(' ', '+').strip()}" + "&" \
                "PastaSearch%5BexibirSomenteDesejos%5D=0&PastaSearch%5BquantidadeRegistro%5D=20"

    url_basdao = "https://mypcards.com/basdao/magic?PastaSearch%5BexibirSomenteVenda%5D=0&PastaSearch" \
                    "%5BexibirSomenteVenda%5D=1&PastaSearch%5Bquery%5D=" + f"{card_name.replace(' ', '+').strip()}" + "&" \
                    "PastaSearch%5BexibirSomenteDesejos%5D=0&PastaSearch%5BquantidadeRegistro%5D=20"
    args = [url, url_wlad, url_basdao]

    card_dict = dict()
    card_list = dict()
    info = ""
    n = 0
    for arg in args:
        card_dict.clear()
        number = 1

        if n == 0:
            loja = "w1"
            nome_loja = "Piedade"
            n = n + 1
        elif n == 1:
            loja = "w0"
            nome_loja = "Wlad"
            n = n + 1
        else:
            loja = "w0"
            nome_loja = "basdao"

        response = re.get(arg).text
        soup = BeautifulSoup(response, "lxml")
        tags = soup.find_all("div", id=loja, class_="row")
        cards = tags[0].find("ul", class_="stream-list")

        try:
            for card in cards:
                items = str(card.text).strip()
                items = items.replace("Comprar", "").replace("Foil", "").replace("un ", "").replace("\xa0", "")

                for lines in items.splitlines():
                    lines = lines.strip()
                    if lines.startswith("R$") is True:
                        info = info + lines
                        card_dict[number] = info
                        number = number + 1
                        info = ""
                        continue
                    if lines == "":
                        continue
                    info = info + lines + "@"
                    card_dict[number] = info
            card_list.update({nome_loja: card_dict.copy()})
        except TypeError:
            card_dict[1] = "Nenhum resultado encontrado"
            card_list[nome_loja] = card_dict.copy()
            continue

    try:
        if card_list["Piedade"][1] == "Nenhum resultado encontrado":
            headers = ["Piedade"]
            values = [["Nenhum resultado encontrado"]]
            print(tabulate(values, headers=headers, tablefmt="grid"))
        else:
            headers = ["Piedade", "Nome PT", "Nome ING", "Coleção", "Qualidade", "Quantidade", "Preço"]
            values = [[key, *value.split("@")] for key, value in card_list["Piedade"].items()]
            print(tabulate(values, headers=headers, tablefmt="grid"))
    except KeyError:
        pass
    try:
        if card_list["Wlad"][1] == "Nenhum resultado encontrado":
            headers = ["Wlad"]
            values = [["Nenhum resultado encontrado"]]
            print(tabulate(values, headers=headers, tablefmt="grid"))
        else:
            headers = ["Wlad", "Nome PT", "Nome ING", "Coleção", "Qualidade", "Quantidade", "Preço"]
            values = [[key, *value.split("@")] for key, value in card_list["Wlad"].items()]
            print(tabulate(values, headers=headers, tablefmt="grid"))
    except KeyError:
        pass
    try:
        if card_list["basdao"][1] == "Nenhum resultado encontrado":
            headers = ["basdao"]
            values = [["Nenhum resultado encontrado"]]
            print(tabulate(values, headers=headers, tablefmt="grid"))
        else:
            headers = ["basdao", "Nome PT", "Nome ING", "Coleção", "Qualidade", "Quantidade", "Preço"]
            values = [[key, *value.split("@")] for key, value in card_list["basdao"].items()]
            print(tabulate(values, headers=headers, tablefmt="grid"))
    except KeyError:
        pass
    return None
