import os
import requests
from bs4 import BeautifulSoup

not_a_technology = ["German", "Polish", "Ukrainian", "English", "French"]

r = requests.get("https://nofluffjobs.com/warszawa/backend?criteria=category%3Dfrontend,fullstack,mobile,testing%20jobLanguage%3Dpl,en,uk,ru%20seniority%3Dtrainee,junior&page=1").text
soup = BeautifulSoup(r, 'html.parser')
jobs_list_div = soup.find("nfj-search-results", {"class", "tw-block tw-mb-5 ng-star-inserted"})
job_links_array = []
number_of_pages = 1
all_musts = {}
all_nices = {}
jobs_list = jobs_list_div.findAll("a")
for job in jobs_list:
    if job.has_attr("href"):
        link_adr = job["href"]
        if "/job/" in link_adr:
            offer_adress = "https://nofluffjobs.com"+link_adr
            if offer_adress not in job_links_array:
                job_links_array.append(offer_adress)
        else:
            if job.text.strip().isnumeric():
                page_number = int(job.text.strip())
                if page_number > number_of_pages:
                    number_of_pages = page_number
def soup_to_offers(soup):
    global job_links_array
    jobs_list_div = soup.find("nfj-search-results", {"class", "tw-block tw-mb-5 ng-star-inserted"})
    jobs_list = jobs_list_div.findAll("a")
    for job in jobs_list:
        if job.has_attr("href"):
            link_adr = job["href"]
            if "/job/" in link_adr:
                offer_adress = "https://nofluffjobs.com" + link_adr
                if offer_adress not in job_links_array:
                    job_links_array.append(offer_adress)


adress_template = "https://nofluffjobs.com/warszawa/backend?criteria=category%3Dfrontend,fullstack,mobile," \
                  "testing%20jobLanguage%3Dpl,en,uk,ru%20seniority%3Dtrainee,junior&page=NUMER_STRONY"
for i in range(2,number_of_pages+1):
    current_adress = adress_template.replace("NUMER_STRONY", str(i))
    request = requests.get(current_adress).text
    try:
        currSoup = BeautifulSoup(request, 'html.parser')
        soup_to_offers(currSoup)
    except:
        print("Nie udało się sparsować {}.".format(current_adress))

def scan_single_offer(adress):
    musts = []
    nices = []
    req = requests.get(adress).text
    soup = BeautifulSoup(req, 'html.parser')
    sections = soup.findAll("section")
    for section in sections:
        if section.has_attr("branch") and section["branch"] == "musts":
            musts_section = section
        if section.has_attr("branch") and section["branch"] == "nices":
            nices_section = section
    must_reqs_lists = musts_section.findAll("li")
    for li in must_reqs_lists:
        requirement = li.text
        requirement = requirement[:-1]
        if requirement[0] == " ":
            requirement = requirement[1:]
        musts.append(requirement)
        if requirement in all_musts:
            all_musts[requirement] += 1
        else:
            all_musts[requirement] = 1
    try:
        nice_reqs_lis = nices_section.findAll("li")
        for li in nice_reqs_lis:
            requirement = li.text
            requirement = requirement[:-1]
            if requirement[0] == " ":
                requirement = requirement[1:]
            nices.append(requirement)
            if requirement in all_nices:
                all_nices[requirement] += 1
            else:
                all_nices[requirement] = 1
    except:
        pass
#remove languages

#scan_single_offer("https://nofluffjobs.com/job/junior-net-developer-eversis-warszawa")
for offer in job_links_array:
    scan_single_offer(offer)
print(all_musts)
print(all_nices)


sorted_musts = sorted(all_musts.items(), key=lambda x:x[1], reverse=True)
sorted_musts = dict(sorted_musts)
print(sorted_musts)
