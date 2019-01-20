from bs4 import BeautifulSoup


def parse(filename, html_body):
    """
    Parser used in warc-parser; parse HTML body of CNN articles.
    :param filename: file name starting with date
    :param html_body: string of HTML
    :return: None, or string of parsed result: date, headline, article body
    """
    def parse_type_1(soup):
        try:
            headline = soup.find("h1", class_="pg-headline").string.strip()
            div_body = soup.find("div", {"itemprop": "articleBody"})
            paras = [el.getText().strip() for el in div_body.find_all(attrs={"class": "zn-body__paragraph"})]
            if len(paras) == 0:
                return None
            body = '\n'.join(paras)
            return headline, body
        except Exception as e:
            return None

    soup_html = BeautifulSoup(html_body, features="lxml")
    parse_types = [parse_type_1]
    result = None
    for parse_type in parse_types:
        if result:
            break
        result = parse_type(soup_html)

    if result:
        date = filename[:len('XXXX-XX-XX')]
        return date + '\n%s\n\n%s' % result
    else:
        return None
