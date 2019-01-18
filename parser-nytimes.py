from bs4 import BeautifulSoup


def parse(filename, html_body):
    """
    Parser used in warc-parser; parse HTML body of NY Times articles.
    :param filename: file name starting with date
    :param html_body: string of HTML
    :return: None, or string of parsed result: date, headline, article body
    """
    def parse_type_1(soup):
        try:
            headline = soup.find(id="headline").string.strip()

            paras = [p.getText().strip() for p in soup.find_all("p", class_="story-content")]
            if len(paras) == 0:
                return None
            body = '\n'.join(paras)
            return headline, body
        except Exception as e:
            return None

    def parse_type_2(soup):
        try:
            headline = soup.find("h1", {"itemprop": "headline"}).getText().strip()

            paras = [p.getText().strip() for p in soup.find("section", {"itemprop": "articleBody"}).find_all("p")]
            if len(paras) == 0:
                return None
            body = '\n'.join(paras)
            return headline, body
        except Exception as e:
            return None

    def parse_type_3(soup):
        try:
            headline = soup.find("h1", {"itemprop": "headline"}).getText().strip()

            paras = []
            divs = soup.find(id="story").find_all("div", class_="StoryBodyCompanionColumn")
            for div in divs:
                paras += [p.getText().strip() for p in div.find_all("p")]
            if len(paras) == 0:
                return None
            body = '\n'.join(paras)
            return headline, body
        except Exception as e:
            return None

    soup_html = BeautifulSoup(html_body, features="lxml")
    result = parse_type_1(soup_html)
    if result is None:
        result = parse_type_2(soup_html)
    if result is None:
        result = parse_type_3(soup_html)

    if result is None:
        return None
    else:
        date = filename[:len('XXXX-XX-XX')]
        return date + '\n%s\n\n%s' % result
