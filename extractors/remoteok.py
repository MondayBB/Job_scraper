from bs4 import BeautifulSoup
import requests


def extract_rmo_jobs(term):
    url = f"https://remoteok.com/remote-{term}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    rmo_results = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        jobs = soup.find_all("tr", class_="job")
        for job in jobs:
            link = job.find("a", itemprop="url")['href']
            company = job.find("h3", itemprop="name")
            position = job.find("h2", itemprop="title")
            location = job.find("div", class_="location")
            if link:
                link = link.strip()
            if company:
                company = company.string.strip()
            if position:
                position = position.string.strip()
            if location:
                location = location.string.strip()

            if company and position and location:
                job = {
                    'link': f"https://remoteok.com{link}",
                    'company': company,
                    'position': position,
                    'location': location
                }
                rmo_results.append(job)
    else:
        print("Can't get jobs.")
    return rmo_results