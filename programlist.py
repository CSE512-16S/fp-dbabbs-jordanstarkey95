from bs4 import BeautifulSoup
import csv, re, requests, itertools, json

# creates json file for program : courses list, used to populate search fields

r = requests.get('https://www.washington.edu/students/crscat/')
courseList = BeautifulSoup(r.content, "html.parser")
links = courseList.findAll("a", {"href" : re.compile("^.*.html$")})

c = {}

for course in links:
    title_search = re.search("[(].*[)]$", course.text)
    if title_search:
        t = title_search.group()
        tindex = t.rfind("(")
        t = t[tindex:]
        t = t.replace("(", "")
        t = t.replace(")", "")
        if t.find("See") is -1:
            c[course['href']] = t

print(json.dumps(c))

url = 'https://www.washington.edu/students/crscat/'

f = {}

for k, y in c.items():
    # list program courses
    p = []

    r = requests.get('https://www.washington.edu/students/crscat/' + k)
    courseList = BeautifulSoup(r.content, "html.parser")
    courses = courseList.select("p")
    # filter courses (skips any <p> that isnt course listing (e.g. course offerings)
    # also eliminates unencoded chars (amp;)
    courses = [x for x in courses if re.match('^' + y + '.*', x.text) and re.sub(r'amp;', '', x.text)]
    for course in courses:
        courseText = re.sub(';', '', course.text)
        title = str(re.search('^' + y + '\s\d{3}', courseText).group())
        title = re.sub("\D", "", title)
        p.append(title)
    f[y.encode('utf-8')] = p

# json output
print(json.dumps(f))


# csv output
with open("programList.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(f.keys())
   writer.writerows(itertools.izip_longest(*f.values()))