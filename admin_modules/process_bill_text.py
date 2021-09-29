import re

date = ""
time = ""
datas = []


def get_txt_file_data(textfile_name):
    global date, time
    datas = []
    with open(textfile_name, "r") as bill:
        for i, line in enumerate(bill):
            # set date
            if "Date" in line:
                date = line[line.index(":") + 1 : line.index("Branch")].replace(" ", "")

            # set time
            elif "Session" in line:
                if "a" in (
                    line.replace("|", "")
                    .replace("Session", "")
                    .replace(" ", "")
                    .lower()
                ):
                    time = "AM"
                else:
                    time = "PM"

            line = line.replace("-", "")
            match_alpha = re.compile("([A-z]+)")
            match_num = re.compile("([0-9]+)")

            # dont forget to add lines without |
            if not match_alpha.findall(line):
                if line.count("|") > 1 and match_num.findall(line):
                    line = (
                        line.replace(",", "")
                        .replace("|", ",")
                        .replace(" ", "")
                        .replace("\n", "")
                        .split(",")
                    )
                    line = [i for i in line if i]
                    if len(line) > 6:
                        datas.append(line)

                elif line.count("|") < 1 and match_num.findall(line):
                    line = line.replace(",", "").replace(" ", ",").split(",")
                    line = [i.replace("\n", "") for i in line if i]
                    if len(line) > 6:
                        datas.append(line)
    if date != "" and time != "":
        print(f"date {date} time {time}")
        return {"datas": datas, "date": date, "time": time}
    else:
        print(f"date {date} time {time}")
        return 0
