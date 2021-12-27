from pip._vendor import requests
from bs4 import BeautifulSoup

from indeed import extract_jobs


HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}

def get_last_page(url):
    result = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(result.text, "html.parser")
    page = soup.find("div", {"class":"s-pagination"})
    if page:    
        links = page.find_all("a")
        links = links[:-1]
        last_page = links[-1].get_text(strip=True)
        return int(last_page)
    else:
        return 0

def extract_job(html):
    title = html.find("h2",{"class":"mb4"}).find("a")["title"]
    # recursive=False 는 span 안쪽에 있는 다른 span 요소까지 가져오지 않게 해줌. (간혹 span이 더 들어가 있는 경우가 있음)
    company, location = html.find("h3", {"class":"fc-black-700"}).find_all("span", recursive=False)
    # strip=True 로 공백 제거 # 줄 바꿈같은 경우, 「\n」「\r」이 존재
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html["data-jobid"]
    return {'title':title, 'company':company, 'location':location, 'link':f'https://stackoverflow.com/jobs/{job_id}'}

def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Stackoverflow page {page}")
        result = requests.get(url=f"{url}&pg={page+1}", headers=HEADERS)
        # print(result.status_code)
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div",{"class":"-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs
        

def get_jobs(job_name):
    url = f"https://stackoverflow.com/jobs?q={job_name}"
    last_page = get_last_page(url)
    if last_page != 0:
        jobs = extract_jobs(last_page, url)
        return jobs
    else:
        return None