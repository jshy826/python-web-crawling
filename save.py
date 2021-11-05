import csv

def save_to_file(jobs):
    # mode 의 w는 쓰기 기능을 의미. r은 읽기
    # open은 파일이 존재하지 않은 경우, 자동으로 생성해줌.
    file = open("jobs.csv", mode="w", encoding="UTF-8", newline="")
    writer = csv.writer(file)
    # 타이틀들을 배열로 넘겨서 작성해줌
    writer.writerow(['title', 'company', 'location', 'link'])
    for job in jobs:
        # key값 말고 value값만 작성
        writer.writerow(list(job.values()))