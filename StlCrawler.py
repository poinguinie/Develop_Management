import re
import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self) -> None:
        self.initVariable()

    def initVariable(self):
        self.homepage = "https://cplusplus.com"
        # self.url = self.homepage + "/reference/" + self.stl + "/" + self.stl + "/"
        self.main_status = 0
        self.detail_status = 0
        self.functions_data = []
        self.detail_data = {}

    def connect(self, stl_type, detailUrl = None):
        self.functions_data = []
        self.detail_data = {}
        url  = self.homepage + "/reference/" + stl_type + "/" + stl_type + "/"
        if detailUrl != None:
            response = requests.get(detailUrl)
            self.detail_status = response.status_code
        else:
            response = requests.get(url)
            self.main_status = response.status_code
            
        if response.status_code == 500:
            response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            if detailUrl != None:
                self.crawlingDetail(soup)
            else:
                self.crawlingSTL(soup)
    
    def crawlingSTL(self, soup):
        functions = soup.find("section", attrs={"id": "functions"}).find_all("dl", attrs={"class": "links"})
        
        for function in functions:
            dt = function.find("dt")

            link = self.homepage + dt.find("a")["href"]
            title = dt.text

            self.functions_data.append({
                "title": title,
                "link": link,
            })

    def crawlingDetail(self, soup):
        title = soup.find("div", attrs={"id": "I_description"}).text
        desc = soup.find("section", attrs={"id": "description"}).text
        param = soup.find("section", attrs={"id": "parameters"})
        if param != None:
            param = param.text.replace("Parameters", "").strip()

        return_value = soup.find("section", attrs={"id": "return"})
        if return_value != None:
            return_value = return_value.text.replace("Return Value", "").strip()
        
        example = soup.find("section", attrs={"id": "example"})

        ex_code = ""
        ex_output = ""
        if example != None:
            ex_code = example.find("td", attrs={"class": "source"})
            ex_output = example.find("td", attrs={"class": "output"})

            if ex_code != None:
                ex_code = ex_code.text
            if ex_output != None:
                ex_output = ex_output.text

        self.detail_data["title"] = title
        self.detail_data["description"] = desc
        self.detail_data["parameters"] = param
        self.detail_data["return_value"] = return_value
        self.detail_data["example_code"] = ex_code
        self.detail_data["example_output"] = ex_output

        # print(self.detail_data)

if __name__ == "__main__":
    crawler = Crawler()
    crawler.connect("vector")
    # print(crawler.functions_data)
    # crawler.connect("vector", "https://cplusplus.com/reference/vector/vector/vector/")

