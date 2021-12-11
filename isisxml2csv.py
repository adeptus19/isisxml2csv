import re
id = 1
def strip_tag(line):
    field = list()
    stripped = line
    stripped = re.search("(^<.+?>)(.+)<.+?>", line)
    if re.match("(^<.+?>)(.+)<.+?>", line):
        tag = stripped.group(1)
        content = stripped.group(2)
        field = [tag, content]
    else:
        return None
    return field


def get_tag(record, tagname):
    if tagname in record.keys():
        return record[tagname]
    else:
        return " "


def write_record(lines, id):
    record = dict()
    csvline = ""
    for line in lines:
        field = strip_tag(line)
        if field is not None:
            if field[0] in record.keys():
                record[field[0]] = record[field[0]] + ":" + field[1]
            else:
                record[field[0]] = field[1]

    tag2 = get_tag(record, "<Tag_2>").split(":")
    if len(tag2) > 1:
        raktj = tag2[0]
    else:
        raktj = " "
    if len(raktj) > 5 and " " in raktj:
        temp = raktj.split(" ")
        szakj = temp[0]
        raktj = temp[1]
        if len (temp) > 2:
            raktj = raktj + temp[2]
    else:
        szakj = ""
    csvline = csvline + str(id) + "|"
    csvline = csvline + szakj + "|"
    csvline = csvline + raktj + "|"
    csvline = csvline + get_tag(record, "<Tag_70>") + "|"
    csvline = csvline + get_tag(record, "<Tag_24>") + "|"
    csvline = csvline + get_tag(record, "<Tag_74>") + "|"
    csvline = csvline + get_tag(record, "<Tag_70>") + "|"
    csvline = csvline + get_tag(record, "<Tag_25>") + "|"
    kiad_ad = get_tag(record, "<Tag_26>")
    temp = kiad_ad.split(",")
    if len(temp) == 3:
        kiadjel = temp[0]
        kiadas = temp[1].strip()
        kiadev = temp[2].strip()
    else:
        kiadjel = ""
        kiadas = ""
        kiadev = temp[0]
    csvline = csvline + kiadjel + "|"
    csvline = csvline + kiadas + "|"
    csvline = csvline + kiadev + "|"
    csvline = csvline + get_tag(record, "<Tag_30>") + "|"
    csvline = csvline + get_tag(record, "<Tag_50>") + "|"
    csvline = csvline + get_tag(record, "<Tag_69>") + "|"
    csvline = csvline + get_tag(record, "<Tag_1>")
    bookfile.write(csvline + "\n")
    kpldline = ""
    if len(tag2) > 1:
        for i in range(1, len(tag2)):
            kpldline = kpldline + tag2[i] + "|"
        kpldline = kpldline.rstrip("|")
    else:
        kpldline = tag2[0]
    kpldtowrite = kpldline.split("|")
    for word in kpldtowrite:
        kpldfile.write(str(id) +"|" + word + "\n")
    id = id + 1
    return id


# input_name  = input("Enter input file name: ")
xmlfile = open("/data/development/winisis_p/KONYV3.xml", encoding="iso-8859-2")
# output_name  = input("Enter output file name: ")
bookfile = open("/data/development/winisis_p/konyvek.csv", "w", encoding="iso-8859-2")
kpldfile = open("/data/development/winisis_p/kpld.csv", "w", encoding = "iso-8859-2")
act_record = list()
last_record = list()
record_line = False
for line in xmlfile:
    if record_line and line.strip() != "</RECORD>" and line.strip() != "":
        act_record.append(line.strip())
    if line.strip() == "<RECORD>":
        record_line = True
    if line.strip() == "</RECORD>":
        record_line = False
        write_record(act_record, id)
        id = id + 1
        act_record = list()
bookfile.close()
kpldfile.close()
xmlfile.close()
