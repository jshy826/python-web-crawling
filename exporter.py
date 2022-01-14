import csv

def save_to_file(jobs, job_name):
    # mode 의 w는 쓰기 기능을 의미. r은 읽기
    # open은 파일이 존재하지 않은 경우, 자동으로 생성해줌.
    file = open(job_name + ".csv", mode="w", encoding="utf-8-sig", newline="")
    writer = csv.writer(file)
    # 타이틀들을 배열로 넘겨서 작성해줌
    writer.writerow(['Title', 'Company', 'Location', 'Link'])
    for job in jobs:
        # key값 말고 value값만 작성
        writer.writerow(list(job.values()))