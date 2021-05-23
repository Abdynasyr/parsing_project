import csv

import requests

from bs4 import BeautifulSoup

def get_html(url):
    response = requests.get(url)
    return response.text

def get_total_pagers(html):
    soup = BeautifulSoup(html,'lxml')
    pages_div = soup.find('div', class_='pager-wrap').find('ul')
    page_li = pages_div.find_all('li') [-1]
    pages_a = page_li.find('a').get('href').split('=') [-1]
  
    return (int(pages_a))

def write_to_csv(data):
    with open('kivano.kg.csv','a') as csv_file:
        writer = csv.writer(csv_file,delimiter='/')
        writer.writerow((data['name'],
                         data['price'],
                         data['photo']))

def get_page_data(html):
    soup = BeautifulSoup(html,'lxml')
    product_list = soup.find('div',class_="list-view")
    # products = product_list.find_all("div", class_="item product_listbox oh")
    # print(product_list)


    for product in product_list:
        try:
            name = product.find('div',class_="listbox_title oh").find('a').text
            # print(name)
        except:
            name = ''
        try:
            price = product.find('div', class_="listbox_price text-center").text
            # print(price)
        except:
            parice = ''
        try:
            photo = product.find('div',class_="listbox_img pull-left").find("a").find("img").get("src")
            
            # print(photo)
        except:
            photo = ''

        data = {'name': name,'price': price,'photo': "https://www.kivano.kg" + photo}
        write_to_csv (data)


def main():
    mobilnye_url = 'https://www.kivano.kg/mobilnye-telefony'
    pages = '?page='
    # get_html(mobilnye_url)
    # get_total_pagers(get_html(mobilnye_url))
    # get_page_data(get_html(mobilnye_url))
    total_pages = get_total_pagers(get_html(mobilnye_url))
    # print(total_pages)

    for page in range(1, total_pages+1):
        url_page = mobilnye_url + pages + str(page)
        # print(url_wiht_page)
        html = get_html(url_page)
        get_page_data(html)
    
main()
