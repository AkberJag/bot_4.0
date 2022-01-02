import re, csv

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
        return {"datas": datas, "date": date, "time": time}
    else:
        return 0


def get_csv_file_data(textfile_name):
    with open(textfile_name, "r") as csv_file:
        csv_data = [element for element in list(csv.reader(csv_file))]
    if len(csv_data) > 0:
        if set(["Pro Id", "Mem No", "Pro Name"]).issubset(csv_data[0]):
            return {"datas": csv_data}
    return 0
