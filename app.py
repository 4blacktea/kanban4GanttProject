from flask import Flask
import os
import datetime
import time

app = Flask(__name__)



@app.route('/')
def index():  # put application's code here
    return '<script>window.location.href="static/index.html"</script>'


@app.route('/html')
def hello_world():  # put application's code here
    htmls = '<h1>项目看板列表</h1><table border="0"><tr><th>项目</th><th>项目进度</th><th>相关人</th><th>开始时间</th><th>预计结束时间</th><th' \
            '>风险节点</th></tr> '
    for project in getprojectlist():
        status, users, starttime, endtime, weektask = getprojectinfo(project.replace(".html", ""))
        htmls = htmls + '<tr><th><a href="static/' + project + '">' + project + '</a></th><th>' + status + '</th><th>' + users + '</th><th>' + starttime + '</th><th>' + endtime + '</th><th>' + weektask + '</th></tr>'
    htmls = htmls + "</table>"
    return htmls


@app.route('/api')
def api():  # put application's code here
    progremlist= []
    htmls = '<h1>项目看板列表</h1><table border="0"><tr><th>项目</th><th>项目进度</th><th>相关人</th><th>开始时间</th><th>预计结束时间</th><th' \
            '>风险节点</th></tr> '
    for project in getprojectlist():
        status, users, starttime, endtime, weektask = getprojectinfo(project.replace(".html", ""))
        status = status.replace("%","")
        print(status)
        addheader(project.replace(".html", ""))
        htmls = htmls + '<tr><th><a href="static/' + project + '">' + project + '</a></th><th>' + status + '</th><th>' + users + '</th><th>' + starttime + '</th><th>' + endtime + '</th><th>' + weektask + '</th></tr>'
        progremlist.append({"project": project.replace(".html", ""), "link": project, "status": status, "users": users, "starttime": starttime, "endtime": endtime, "weektask": weektask})
    htmls = htmls + "</table>"
    print(progremlist)
    return {"data": progremlist}

def addhewaerfile(filename):
    f = open("static/" + filename, "r")
    filedata = f.read()
    f.close()
    print(filedata)
    if "F56C6C" not in filedata:
        raw = '<body bgcolor="white">'
        rep = '<body bgcolor="white"><h1 onclick=\'window.location.href="index.html"\' style="display: block; font-size: 2em; margin-block-start: 0.67em; margin-block-end: 0.67em; margin-inline-start: 0px; margin-inline-end: 0px; font-weight: bold;"><font color="#F56C6C">项目看板</font></h1>'
        filedata = filedata.replace(raw, rep)
        f1 = open("static/" + filename, "w")
        f1.write(filedata)
        f1.close()

def addheader(project):
    fileends = ['.html', '-chart.html', '-resources.html', '-tasks.html']
    for i in fileends:
        addhewaerfile(project + i)


def getprojectlist():
    filepath = "static/"
    # 遍历filepath下所有文件，包括子目录
    filelist = []
    files = os.listdir(filepath)
    for file in files:
        #print(file)
        if file.split("-")[-1] == 'tasks.html':
            filelist.append(file.replace('-tasks.html','.html'))
    #print(filelist)
    return filelist


def formatdate(indate):
    redate = ""
    for i in indate.split("/"):
        #print(i)
        if len(i) == 1:
            redate = redate + '0' + i
        else:
            redate = redate + i
    redate = redate[:4] + "/" + redate[4:6] + "/" + redate[6:]
    #print(redate)
    return redate


def getprojectinfo(projectname):
    tasklist = []
    userlist = []
    csvfile = open('static/' + projectname + '.csv')
    #print("\n\n------")
    flag = 0
    for i in csvfile.readlines():
        if i.strip() == '"序号",名称,开始日期,结束日期,持续,完成,成本,协调者,前置任务,大纲编号,资源,Assignments,新任务,网页连接,备注':
            flag = 1
        elif i.strip() == '"序号",名称,默认角色,电子邮件,电话,成本标准,总成本,总负荷':
            flag = 2
        else:
            if flag == 1 and len(i.strip().split(',')) != 1:
                print(i.strip().split(','))
                tasklist.append(i.strip().split(','))
            if flag == 2 and len(i.strip().split(',')) != 1:
                #print(i.strip().split(','))
                userlist.append(i.strip().split(','))
    alltime = 0

    donetime = 0
    starttimes = []
    endtimes = []
    weektask = ""
    users = ''
    today = str(datetime.date.today()).replace("-","/")
    print(today)
    for i in tasklist:
        alltime = alltime + int(i[4])
        donetime = donetime + int(i[4]) * int(i[5])
        starttimes.append(formatdate(i[2]))
        endtimes.append(formatdate(i[3]))
        if today > formatdate(i[3]) and i[5] != "100":
            weektask = weektask + i[1] + ", "

    for j in userlist:
        users = users + j[1] + '  '
    #print(starttimes)
    #print(min(starttimes))
    #print(max(endtimes))
    #print(alltime)
    #print(donetime)
    #print("%.2f%%" % (donetime/alltime))
    #print(userlist)
    if weektask == "":
        weektask = "暂无"

    return ["%.2f%%" % (donetime/alltime), users, min(starttimes), max(endtimes), weektask]


if __name__ == '__main__':
    app.run()




