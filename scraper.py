from bs4 import BeautifulSoup
import re, requests, json, pickle, glob, csv

url = 'https://www.washington.edu/students/crscat/'
'''
# Beautiful soup object initialize and request
r = requests.get(url)
courseList = BeautifulSoup(r.content, "html.parser")
links = courseList.findAll("a", {"href" : re.compile("^.*.html$")})

# Create a dict of "url":"Program"
c = {}
for course in links:
    title_search = re.search("[(].*[)]", course.text)
    if title_search:
        t = title_search.group()
        tindex = t.rfind("(")
        t = t[tindex:]
        t = t.replace("(", "")
        t = t.replace(")", "")
        if t.find("See") is -1:
            c[course['href']] = t
print(json.dumps(c))
'''
'''
# read in courseURL.json
with open('courseURL.json') as data_file:
    data = json.load(data_file)
# creates json file for program : courses list, used to populate search fields and create programList.json
f = {}
for k, y in data.items():
    # list program courses
    p = []

    y = str(y.encode('utf-8'))
    k = str(k.encode('utf-8'))

    r = requests.get(url + k)
    courseList = BeautifulSoup(r.content, "html.parser")
    courses = courseList.select("p")
    # filter courses (skips any <p> that isnt course listing (e.g. course offerings)
    # also eliminates unencoded chars (amp;)
    # skip p tag with course offerings
    for course in courses[1:]:
        courseText = re.sub(';', '', course.text)
        title = courseText[:len(y) + 4].strip()
        courseNum = re.sub(r'\D', '', title)
        p.append(courseNum)
    f[y] = p
'''
'''
# csv output
with open("programList.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(f.keys())
   writer.writerows(itertools.izip_longest(*f.values()))
'''
'''
# json
with open('programList.json', 'w') as outfile:
    json.dump(f, outfile)

print(json.dumps(f))

'''
'''
# For each url,program courseURL in dict
for k, y in data.items():

    k = str(k.encode('utf-8'))
    y = str(y.encode('utf-8'))

    # request url of this program
    r = requests.get('https://www.washington.edu/students/crscat/' + k)
    courseList = BeautifulSoup(r.content, "html.parser")
    courses = courseList.select("p")

    # master list containing dicts of every class in that program
    p = []
    # for every course in program course list
    for course in courses[1:]:

        # retrieve text inside html tags, stripping ; for unicode purposes
        courseText = re.sub(';', '', course.text)
        # retrieve title of this course
        title = courseText[:len(y) + 4].strip()
        c = {"name": title}

        # provide this for hyperlink?
        # Strip myPlan hyperlink from course description
        linkIndex = courseText.rfind("View course details in MyPlan:")
        courseText = courseText[:linkIndex]

        # Get b tag in course, contains course title, credit, and credit type
        courseInfo = course.select("b")
        # check if courses exist
        if len(courseInfo) > 0:
            courseInfo = courseInfo[0].text
        else:
            print course
            break

        # COURSE INFO STRIPPING
        # course title
        courseTitleIndex = courseInfo.find("(")
        courseTitle = courseInfo[:courseTitleIndex]
        c["course_title"] = courseTitle
        courseText = courseText.replace(c["course_title"], "")
        # course credit
        courseCreditIndex = courseInfo.find(")")
        c["credits"] = courseInfo[courseTitleIndex:courseCreditIndex + 1]
        courseText = courseText.replace(c["credits"], "")
        # course credit type
        c["credit_type"] = courseInfo[courseCreditIndex + 1:]
        courseText = courseText.replace(c["credit_type"], "")
        # Professor
        courseProf = course.select("i")
        professors = ""
        if len(courseProf) > 0:
            professors = courseProf[0].text
        c["professors"] = professors
        courseText = courseText.replace(c["professors"], "")


        # offered with case (list of classes offered jointly with)
        offeredIndex = courseText.rfind("Offered: jointly with")
        offered = []
        if offeredIndex != -1:
            courseText = courseText[:offeredIndex]
            offered = re.findall('[A-Z]+\s?[A-Z]\s+\d{3}', courseText[offeredIndex:])
        c["offered_with"] = offered

        # Course description after stripped of credt, title, offered, credit type
        c["description"] = courseText

        # prerequsites
        preqIndex = courseText.rfind("Prerequisite:")
        choice_preqList = []
        required_preqList = []

        # if prerequsites exist, filter them into choice or required and add class attributes
        if preqIndex != -1:

            c["description"] = courseText[:preqIndex]

            # strip char punctuations
            coursePreq = re.sub('[:.;,]', '', courseText[preqIndex:])

            # either case ALWAYS comes after required preqs, used find instead of rfind cause either can repeat
            # what if either appears in course description? may have to remove
            eitherIndex = courseText.find("either")

            required_prereqs = []
            # if either case exists, add to choice prereqs list
            if eitherIndex != -1:
                required_prereqs = re.findall('[A-Z]+\s?[A-Z]\s+\d{3}', coursePreq[:coursePreq.find("either")])

                choice_preqreqs = re.findall('[A-Z]+\s?[A-Z]\s+\d{3}', courseText[eitherIndex:])
                for choice_preqreq in choice_preqreqs:
                    choice_preqList.append({"name": choice_preqreq})

            else:
                required_prereqs = re.findall('[A-Z]+\s?[A-Z]\s+\d{3}', coursePreq)

            for required_prereq in required_prereqs:
                required_preqList.append({"name": required_prereq})

        c["choice_prereqs"] = choice_preqList
        c["required_prereqs"] = required_preqList

        p.append(c)

    f = p

    def recurse(m, is_preqFor):
        for h in reversed(f):
            if any(g["name"] == m["name"] for g in h["required_prereqs"]):
                h["type"] = "required"
                is_preqFor.append(h)
                f.remove(h)
                recurse(h, [])
            # Append choice prereqs to children, give them choice attribute for color encoding
            elif any(g["name"] == m["name"] for g in h["choice_prereqs"]):
                h["type"] = "choice"
                is_preqFor.append(h)
        # append children to course if they exist
        m["children"] = is_preqFor

    # beginning of recursive call
    for d in f:
        recurse(d, [])

    # write each program to json file
    try:
        outfile = open('output' + y + '.json', 'w')
        json.dump(f, outfile)
        outfile.close()
    except ValueError:
        print f
'''

# different output formats
'''
# handle circular reference errors
with open('data.txt', 'w') as outfile:
    for l in programDict:
        outfile.write(l)
'''

'''
    file = open('output' + y + '.json', 'w')
    file.write(str(f))
    file.close()
'''

'''
with open("programSequences.txt", 'wb') as f:
    for p in programDict:
        f.write(p)
'''

'''
filehandler = open("programSequences.pickle","wb")
pickle.dump(programDict, filehandler)
filehandler.close()
'''


# validate json files test
read_files = glob.glob("output*.json")
output_list = []

for f in read_files:
    with open(f, "rb") as infile:
        title = infile.name[6:].replace(".json", "")
        try:
            output_list.append({title: json.load(infile)})
        except ValueError:
            print infile.text
            pass


# merge all program files
with open("merged_file.json", "wb") as outfile:
    json.dump(output_list, outfile)
