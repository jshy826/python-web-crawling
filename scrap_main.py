from flask import Flask, render_template, request, redirect, send_file
from scrap_so import get_jobs as so_get_jobs
from scrap_indeed import get_jobs as indeed_get_jobs
from exporter import save_to_file
import datetime

# 서버 구축
app = Flask("Scrapper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/report")
def report():
    job_name = request.args.get("job-name")
    jobs_total = 0
    if job_name:
        job_name = job_name.lower()
        fromDB = db.get(job_name)
        if fromDB:
            jobs = fromDB
            jobs_total = len(jobs)
        else:
            so_jobs = so_get_jobs(job_name)
            jobs = []
            if so_jobs:
                jobs = so_jobs
            indeed_jobs = indeed_get_jobs(job_name)
            if indeed_jobs:
                jobs += indeed_jobs
            if jobs:
                db[job_name] = jobs
                jobs_total = len(jobs)
            else:
                return redirect("/")   
    else:
        return redirect("/")
    
    # html 에서 쓸 변수는 html 지정 뒤에 인수명을 지정하고 넣어줌
    return render_template("report.html", 
    searchingBy=job_name, 
    resultsNumber=jobs_total,
    jobs=jobs)

@app.route("/export")
def export():
    try:
        job_name = request.args.get("job-name")
        if not job_name:
            raise Exception()
        job_name = job_name.lower()
        jobs = db.get(job_name)
        if not jobs:
            raise Exception()
        save_to_file(jobs, job_name)
        today = datetime.datetime.now()
        csv_file_name = f"{job_name}_{today.year}.{today.month}.{today.day}_jobs.csv"
        return send_file(f"{job_name}.csv", as_attachment = True, attachment_filename = csv_file_name)
    except:
        return redirect("/")
# repl.it 의 경우, run 안에 host="0.0.0.0"을 써서 웹사이트를 공개해줘야함
app.run()