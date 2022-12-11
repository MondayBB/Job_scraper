from bs4 import BeautifulSoup
import requests


def extract_wwr_jobs(term):
    url = f"https://weworkremotely.com/remote-jobs/search?&term={term}"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    wwr_results = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        jobs = soup.find_all("section", class_="jobs")
        for job in jobs:
            jobs_list = job.find_all("li")
            for job_list in jobs_list:
                link = job_list.find("a", recursive=False)
                company = link.select_one("span:nth-of-type(1)")
                position = job_list.find("span", class_="title")
                location = job_list.find("span", class_="region")
                if link:
                    link = link['href'].strip()
                if company:
                    company = company.string.strip()
                if position:
                    position = position.string.strip()
                if location:
                    location = location.string.strip()

                if company and position and location:
                    job = {
                        'link': f"https://weworkremotely.com{link}",
                        'company': company,
                        'position': position,
                        'location': location
                    }
                    wwr_results.append(job)
    else:
        print("Can't get jobs.")
    return wwr_results