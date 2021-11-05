from pip._vendor import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://jp.indeed.com/jobs?q=python&limit={LIMIT}"
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}

def get_last_page():
    result = requests.get(url=URL, headers=HEADERS)

    soup = BeautifulSoup(result.text, "html.parser")
    total_job = get_total_job(soup)
    if(total_job > 1000):
        max_page = 20
    elif(total_job < 1000 and total_job > 250):
        max_page = (total_job // 50) + 1
    else:
        pagination = soup.find("div", {"class":"pagination"})
        links = pagination.find_all('a')
        pages = []
        for link in links[:-1]:
            pages.append(int(link.find("span").string))
        # 마지막 페이지 숫자 가져오기
        max_page = pages[-1]
    return max_page

    # 마지막 데이터를 제외하고 다 가져온다는 것을 의미
    # print(spans[0:-1]) 는 0부터 마지막직전까지 가져옴을 의미
    # print(spans[:-1])

def extract_job(html):
    title = html.find("h2", {"class":"jobTitle"}).find("span", title=True).string
    company = html.find("span", {"class":"companyName"})
    if company is None:
        company = html.find("span", {"class":"company"})
    if company is not None:
        company_anchor = company.find("a")
    else:
        company_anchor = None
    if company:
        if company_anchor is not None:
            company = company_anchor.string
        else:
            company = company.string
    location = html.find("div", {"class":"companyLocation"}).text
    link = html.find_parent("a",{"class":"tapItem"})
    link = link["data-jk"]
    return {'title':title, 'company':company, 'location':location, 'link':f'https://jp.indeed.com/viewjob?jk={link}'}

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping indeed page {page}")
        result = requests.get(url=f"{URL}&start={page*LIMIT}", headers=HEADERS)
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"job_seen_beacon"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs

# 전체 검색 결과 건 수 취득
def get_total_job(soup):
    search_count = soup.find("div", {"id":"searchCountPages"}).string.strip("\n").strip(" ")
    total_job = search_count.split(" ")
    total_job_val = int(total_job[1].replace(",", ""))
    return total_job_val