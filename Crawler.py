import re
import requests
from bs4 import BeautifulSoup

class Crawler:
    # Generator Method
    def __init__(self, url, lang):
        self.url = url
        self.lang = lang
        self.initVar()
        self.status_code = self.connect()
        if self.status_code != 200:
            print("에러 처리")

        # self.makeMainFunction()
        # self.printInfo()

    # Initialize Variable Method
    def initVar(self):
        self.code = ""
        self.title = ""
        self.problem_desc = ""
        self.example_desc = []
        self.restrictions = []
        self.ioExample_list = []
    
    # Connect URL Method
    def connect(self):
        response = requests.get(self.url + "?language=" + self.lang)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            self.crawling(soup)                

        return response.status_code
    
    # Crawling from URL Method
    def crawling(self, soup):
        # Get Code
        self.code = soup.find("textarea", attrs={"id":"code"}).text
        
        # Get Title
        self.title = soup.find(attrs={"class":"algorithm-title"}).text.strip()

        # Get Description
        desc_area = soup.find(attrs={"class":"guide-section-description"}).find("div")

        restrictions_area = soup.find(attrs={"class":"guide-section-description"}).find("ul")
        self.restrictions = [text for text in restrictions_area.text.split("\n") if text]
        # print(self.restrictions)

        desc_detail = desc_area.find_all("p")

        self.problem_desc = []
        i = 0
        for detail in desc_detail:
            if detail.text.find("입출력 예") != -1:
                break
            self.problem_desc.append(detail)
            i += 1

        self.example_desc = desc_detail[i:]

        li1 = []
        li2 = []
        for desc in self.problem_desc:
            item = str(desc).split("<br/>")
            for line in item:
                if line.find("<img ") == -1:
                    line = self.clearHtmlTag(line).strip().replace(".", ".\n").replace(".\n ", ".\n")
                    li1.append(line)
                else:
                    url_start = line.find("https://")
                    url_end = line.find(".png", url_start) + 4
                    li1.append("image_url:" + line[url_start:url_end])

        for desc in self.example_desc:
            item = str(desc).split("<br/>")
            for line in item:
                if line.find("<img ") == -1:
                    li2.append(self.clearHtmlTag(line).strip())
                else:
                    url_start = line.find("https://")
                    url_end = line.find(".png", url_start) + 4
                    li2.append("image_url:" + line[url_start:url_end])

        self.problem_desc = li1
        self.example_desc = li2

        # Get Input Output Example
        ioExample_title = desc_area.find("table").find("thead").find("tr").find_all("th")
        ioExample = desc_area.find("table").find("tbody").find_all("tr")
        
        self.ioExample_list.append([th.text for th in ioExample_title])
            
        for row in ioExample:
            line = []
            columns = row.find_all("td")
            for column in columns:
                line.append(column.text)
            self.ioExample_list.append(line)
    
    # Print Information Method
    def printInfo(self):
        # Information List
        # Title, Problem Description, Example Description, Restrictions, Codes, Input Output Examples
        print(self.title)
        print(self.problem_desc)
        for item in self.example_desc:
            print(item)
        for item in self.restrictions:
            print(item)
        print(self.code)
        print(self.ioExample_list)

    # Prettier the String Data Method
    def prettier(self, data):
        result = []
        for d in data:
            d = d.text
            d = d.split("\n")
            d = [n for n in d if n]
            d = "\n".join(d)
            result.append(self.clearHtmlTag(d))
        return result

    # Make Main Function Method
    def makeMainFunction(self):
        if self.lang != "cpp":
            print("지원하지 않는 언어입니다.")
            return False

        # Get Result Type
        _code = self.code.replace("\r", "")
        _code = _code.split("\n")
        line = _code[5]
        solution_idx = line.find("solution")

        result_type = line[0:solution_idx]

        # Get IO Example Type & Value
        io_examples = []
        for i, ex in enumerate(self.ioExample_list[0]):
            if ex == "result":
                ex = "results"
            info = {
                "title": ex,
                "vector": self.getVectorCount(self.ioExample_list[1][i]) + 1,
                "type": self.getType(self.ioExample_list[1][i]),
                "data": self.formatBracket(self.ioExample_list[1:][i]),
            }
            io_examples.append(info)

        var = ""
        solution = "solution("
        for example in io_examples:
            if example["title"] != "results":
                solution += example["title"]
                solution += "[i], "
            var += "\t"
            var += self.getVectorType(example["vector"], example["type"])
            var += " "
            var += example["title"] + " = "
            if example["vector"] == 1:
                var += "{ "
            for i in range(example["vector"] - 1):
                var += "{ "
            for data in example["data"]:
                var += data
                var += ", "
            for i in range(example["vector"] - 1):
                var += "}, "
            var = var[0: -2]
            if example["vector"] == 1:
                var += " }"
            if self.lang != "python3":
                var += ";\n"   

        solution = solution[0:-2]
        solution += ");"

        self.code = "#include <iostream>\n" + self.code
        self.main_function = ""

        # 4차원 벡터까지 지원
        var_list = ["i", "j", "k", "l"]

        print_result = ""
        if result_type.count("<") == 0:
            print_result += "cout << (i + 1) << \") \" << result << endl;"
            # print_result += "for(int %s = 0; %s < result.size(); %s++) {\n" \
            #     % (var_list[i], var_list[i], var_list[i])
        else :
            print_result += "for(int %s = 0; %s < result[%s].size(); %s++) {\n" \
                % (var_list[0], var_list[0], var_list[0], var_list[0])
            for i in range(1, result_type.count("<")):
                print_result += "\tfor(int %s = 0; %s < result[%s].size(); %s++) {\n" \
                % (var_list[i], var_list[i], var_list[i] ,var_list[i])
            print_result += "\t" * (result_type.count("<") + 2) + "cout << result"
            for i in range(result_type.count("<")):
                print_result += "[" + var_list[i]
            for i in range(result_type.count("<")):
                print_result += "]"
            print_result += " << endl;\n"
        if result_type.count("<") != 0:
            for i in range(result_type.count("<")):
                print_result += "\t" * (result_type.count("<") - i + 1) + "}\n"

        if self.lang == "cpp":
           self.main_function = '''
\nint main(void) {
\t// 입출력 변수 선언
%s
\tint i, size = results.size();

\tfor(i = 0; i < size; i++) {
\t\t%sresult = %s

\t\t%s
\t}
}
           ''' % (var, result_type, solution, print_result)
           # print(self.main_function)

    # Set Main Function Mathod
    def setMainFunction(self):
        response = self.makeMainFunction()
        if response == False:
            return False
        self.code += self.main_function

    # Clear HTML Tag (<div> ... ) Method
    def clearHtmlTag(self, str):
        return re.sub('(<([^>]+)>)', '', str)
    
    # Get Vector Count from Item Method
    def getVectorCount(self, item):
        return item.count("[")

    # Get Item's Variable Type Method
    def getType(self, item):
        if "\"" in item:
            return "str"
        elif "." in item:
            return "double"
        else:
            return "int"
        
    # Get Vector Type using Count, Type Method
    def getVectorType(self, count, type):
        line = ""
        for i in range(count):
            line += "vector<"
        if type == "str":
            line += "string"
        elif type == "double":
            line += "double"
        else:
            line += "int"
        for i in range(count):
            line += ">"
        return line
    
    # Formatting Bracket (python : [], C, C++ : {} ) Method
    def formatBracket(self, data):
        if self.lang == "python3":
            return data
        
        result = []
        
        for d in data:        
            result.append(d.replace("[", "{").replace("]", "}")) 

        return result

if __name__ == "__main__":
    crawler = Crawler("https://school.programmers.co.kr/learn/courses/30/lessons/154539", "cpp")
    # crawler = Crawler("https://school.programmers.co.kr/learn/courses/30/lessons/181186", "cpp")