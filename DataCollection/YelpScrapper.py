import re
import datetime
import pandas as pd
import random
import requests
import urllib
from lxml import html
from time import sleep
from datetime import datetime

def get_parser(url):
    response = requests.get(url).text
    parser = html.fromstring(response)
    return parser

def business_info_scrapper(parser):
    raw_name = parser.xpath("//h1[contains(@class,'page-title')]//text()")
    raw_claimed = parser.xpath("//span[contains(@class,'claim-status_icon--claimed')]/parent::div/text()")
    raw_reviews = parser.xpath("//div[contains(@class,'biz-main-info')]//span[contains(@class,'review-count rating-qualifier')]//text()")
    raw_category  = parser.xpath('//div[contains(@class,"biz-page-header")]//span[@class="category-str-list"]//a/text()')
    hours_table = parser.xpath("//table[contains(@class,'hours-table')]//tr")
    details_table = parser.xpath("//div[@class='short-def-list']//dl")
    raw_map_link = parser.xpath("//a[@class='biz-map-directions']/img/@src")
    raw_phone = parser.xpath(".//span[@class='biz-phone']//text()")
    raw_address = parser.xpath('//div[@class="mapbox-text"]//div[contains(@class,"map-box-address")]//text()')
    raw_wbsite_link = parser.xpath("//span[contains(@class,'biz-website')]/a/@href")
    raw_price_range = parser.xpath("//dd[contains(@class,'price-description')]//text()")
    raw_health_rating = parser.xpath("//dd[contains(@class,'health-score-description')]//text()")
    rating_histogram = parser.xpath("//table[contains(@class,'histogram')]//tr[contains(@class,'histogram_row')]")
    raw_ratings = parser.xpath("//div[contains(@class,'biz-page-header')]//div[contains(@class,'rating')]/@title")
    raw_neighborhood = parser.xpath("//div[@class='map-box-address u-space-l4']/span[@class='neighborhood-str-list']//text()")
    report = parser.xpath('//p[contains(@class,"alert-message text-centered")]/b/text()')
    working_hours = []

    for hours in hours_table:
        raw_day = hours.xpath(".//th//text()")
        raw_timing = hours.xpath("./td//text()")
        day = ''.join(raw_day).strip()
        timing = ''.join(raw_timing).strip()
        working_hours.append({day:timing})
    info = []
    for details in details_table:
        raw_description_key = details.xpath('.//dt//text()')
        raw_description_value = details.xpath('.//dd//text()')
        description_key = ''.join(raw_description_key).strip()
        description_value = ''.join(raw_description_value).strip()
        info.append({description_key:description_value})

    ratings_histogram = []
    for ratings in rating_histogram:
        raw_rating_key = ratings.xpath(".//th//text()")
        raw_rating_value = ratings.xpath(".//td[@class='histogram_count']//text()")
        rating_key = ''.join(raw_rating_key).strip()
        rating_value = ''.join(raw_rating_value).strip()
        ratings_histogram.append({int(rating_key[0]):int(rating_value)})

    name = ''.join(raw_name).strip()
    phone = ''.join(raw_phone).strip()
    address = ' '.join(' '.join(raw_address).split())
    health_rating = ''.join(raw_health_rating).strip()
    price_range = ''.join(raw_price_range).strip()
    claimed_status = ''.join(raw_claimed).strip()
    category = ','.join(raw_category)
    cleaned_ratings = ''.join(raw_ratings).strip()

    if raw_wbsite_link:
        #pass
        decoded_raw_website_link = urllib.parse.unquote(raw_wbsite_link[0])
        website = re.findall("biz_redir\?url=(.*)&website_link",decoded_raw_website_link)[0]
    else:
        website = ''

    if raw_map_link:
        decoded_map_url =  urllib.parse.unquote(raw_map_link[0])
        map_coordinates = re.findall("([+-]?\d+.\d+,[+-]?\d+\.\d+)",decoded_map_url)[0].split(',')
        latitude = float(map_coordinates[0])
        longitude = float(map_coordinates[1])
    else:
        latitude = ''
        longitude = ''

    if raw_ratings:
        ratings = float(re.findall("\d+[.,]?\d+",cleaned_ratings)[0])
    else:
        ratings = 0

    if raw_neighborhood:
        neighborhood = ''.join(raw_neighborhood).strip()
    else:
        neighborhood = ''

    if raw_reviews:
        reviews = int(''.join(raw_reviews).strip().replace(' reviews','').replace(' review',''))
    else:
        reviews = ''

    if report == []:
        permanently_closed = 0
    else:
        permanently_closed = 1

    data={'working_hours':working_hours,
        'info':info,
        'ratings_histogram':ratings_histogram,
        'name':name,
        'phone':phone,
        'ratings':ratings,
        'address':address,
        'health_rating':health_rating,
        'price_range':price_range,
        'claimed_status':claimed_status,
        'reviews':reviews,
        'category':category,
        'website':website,
        'latitude':latitude,
        'longitude':longitude,
        'neighborhood': neighborhood,
        'permanently_closed': permanently_closed
         }
    return data

def get_all_reivews(parser):
    '''Given the parsed first webpage of a restaurant on yelp, return all reviews of that restaurants'''
    review_dict = {'date': [], 'star': [], 'text': []}

    review_dates = parser.xpath("//div[@class='review-content']//span[@class='rating-qualifier']")
    for d in review_dates:
        date = ''.join(d.xpath(".//text()")).strip().split('\n')[0]
        review_dict['date'].append(date)

    review_stars = parser.xpath("//div[@class='review review--with-sidebar']/div[@class='review-wrapper']/div[@class='review-content']/div[@class='biz-rating biz-rating-large clearfix']")
    for s in review_stars:
        star = float(''.join(s.xpath(".//@title")).strip().replace(' star rating',''))
        review_dict['star'].append(star)

    review_texts = parser.xpath("//div[@class='review review--with-sidebar']/div[@class='review-wrapper']/div[@class='review-content']/p")
    for t in review_texts:
        text = ' '.join(t.xpath(".//text()"))
        review_dict['text'].append(text)

    review = pd.DataFrame(review_dict)
    review['date'] =  pd.to_datetime(review['date'])

    review_pages_section = parser.xpath("//div[@class='arrange arrange--stack arrange--baseline arrange--6']//text()")
    review_pages = [item for item in [e.replace('\n','').replace(' ','') for e in review_pages_section] if item != '' ]

    if 'Next' not in review_pages:
        return review
    else:
        nextpage = parser.xpath('//a[@class="u-decoration-none next pagination-links_anchor"]/@href')[0]
        nextparser = get_parser(nextpage)
        sleep(1)
        return review.append(get_all_reivews(nextparser), ignore_index=True)

def get_one_restaurant(path='./', number=None, keyword=None, get_reviews=True):
    bad = 0
    yelp_url = 'https://www.yelp.com/biz/'
    review_start = datetime.strptime('1/1/2010', '%m/%d/%Y')
    url = yelp_url + keyword + '?sort_by=date_asc&start=0'
    #url = yelp_url + keyword + '-chicago' + postfix
    response = requests.get(url)
    sleep(1)
    if response.status_code == 200:
        parsed = html.fromstring(response.text)
        review_dates = parsed.xpath("//div[@class='review-content']//span[@class='rating-qualifier']")
        try:
            first_reviewdate = ''.join(review_dates[0].xpath(".//text()")).strip().split('\n')[0]
            first_datetime = datetime.strptime(first_reviewdate, '%m/%d/%Y')
            if first_datetime <= review_start:
                data = business_info_scrapper(parsed)
                restaurant = pd.DataFrame({k:[v] for k, v in data.items()})
                restaurant['url'] = url
                restaurant.to_csv(path+str(number)+'_'+keyword+'.csv', index=False)
                if get_reviews:
                    reviews = get_all_reivews(parsed).sort_values(by='date', ascending=False).reset_index(drop=True)
                    reviews.to_csv(path+str(number)+'_'+keyword+'_review.csv', index=False)
                print('got '+str(number)+': '+url)
            else:
                print('skip '+str(number)+': '+url)
        except:
                print('problematic reviews '+str(number)+': '+url)
    else:
        bad = 1
        print('didn\'t get '+str(number)+': '+url)
    return bad

def get_all_restaurants(path='./',listfile='./keywords_nochain.txt', start=0, end=None, get_reviews=True):
    restaurants = [line.strip() for line in open(listfile)]
    if end == None:
        end = len(restaurants)
    if start == 0 :
        file = open("did_not_work.txt", "w+")
        file.close()
    for i, keyword in enumerate(restaurants[start:end]):
        number = i + start
        bad = get_one_restaurant(path=path, number=number, keyword=keyword, get_reviews=get_reviews)
        if bad == 1:
            with open("did_not_work.txt","a+") as file:
                file.write(str(number)+': '+keyword+'\n')
        sleep(random.choice([1,2]))


#get_all_restaurants(path='./',listfile='./keywords.txt', get_reviews=True)
