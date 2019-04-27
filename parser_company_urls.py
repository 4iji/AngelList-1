import json

import requests
import scrapy


def get_token(_location, _page, _sort):
    response = requests.post(
        "https://angel.co/company_filters/search_data"
        "?filter_data%5Blocations%5D%5B%5D={}"
        "&sort={}"
        "&page={}".format(
            _location, _sort, _page))
    selector = scrapy.Selector(response)

    _token = selector.xpath("//meta[@name='csrf-token']/@content").extract_first()
    return _token


def get_ids(_location, _page, _token, _sort):
    headers = {"x-csrf-token": _token}
    response = requests.get(
        "https://angel.co/company_filters/search_data"
        "?filter_data%5Blocations%5D%5B%5D={}"
        "&sort={}"
        "&page={}".format(
            _location, _sort, _page), headers=headers)
    return response.content


def parse_json(_json):
    _ids = _json['ids']
    _total = _json['total']
    _hexdigest = _json['hexdigest']

    return _ids, _total, _hexdigest


def get_names_from_ids(_ids, _total, _page, _hexdigest, _token, _sort):
    headers = {"x-csrf-token": _token,
               "x-requested-with": "XMLHttpRequest"}
    base_url = "https://angel.co/companies/startups"
    for _number, _id in enumerate(_ids):
        if _number == 0:

            base_url += "?ids%5B%5D={}".format(_id)
        else:
            base_url += "&ids%5B%5D={}".format(_id)
    base_url += "&total={}&page={}&sort={}&new=false&hexdigest={}".format(_total, _page, _sort, _hexdigest)
    response = requests.get(base_url, headers=headers)
    return response.content.decode("utf-8")


def get_links(response_html):
    _json = json.loads(response_html)
    selector = scrapy.Selector(text=_json["html"])
    links_tags = selector.xpath("//div[@class='photo']/a[@class='startup-link']")
    start_ups = list()
    for each in links_tags:
        data_link = each.xpath("./@href").extract_first()
        data_id = each.xpath("./@data-id").extract_first()
        start_ups.append((data_link, data_id))
    return start_ups


locations = ['2003-Egypt', '10712-Saudi Arabia', '2069-United Arab Emirates']
sorting = ['signal', 'raised', 'joined']

for location in locations:
    for sort_type in sorting:
        page = 1
        while page < 21:
            print("{} Page: {}".format(location, page))
            token = get_token(location, page, sort_type)
            ids_response = get_ids(location, page, token, sort_type)
            ids_json = json.loads(ids_response)
            print(ids_json)
            ids, total, hexdigest = parse_json(ids_json)
            if not ids:
                break
            titles = get_names_from_ids(ids, total, page, hexdigest, token, sort_type)

            companies = get_links(titles)
            with open('company_urls.txt', 'a') as _output_file:
                for company in companies:
                    _output_file.write(company[0] + '\n')
            print(companies)
            page += 1
