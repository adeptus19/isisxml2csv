import re


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
        return ""
    return


def write_record(lines):
    record = dict()
    csvline = ""
    for line in lines:
        field = strip_tag(line)
        if field is not None:
            if field[0] in record.keys():
                record[field[0]] = record[field[0]] + ":" + field[1]
            else:
                record[field[0]] = field[1]
    lszam = get_tag(record, "<Tag_2>").split(":")[0]
    csvline = csvline + lszam + ", "
    csvline = csvline + get_tag(record, "<Tag_70>") + ", "
    csvline = csvline + get_tag(record, "<Tag_24>") + ", "
    csvline = csvline + get_tag(record, "<Tag_74>") + ", "
    csvline = csvline + get_tag(record, "<Tag_70>") + ", "
    csvline = csvline + get_tag(record, "<Tag_25>") + ", "
    csvline = csvline + get_tag(record, "<Tag_26>") + ", "
    csvline = csvline + get_tag(record, "<Tag_30>") + ", "
    csvline = csvline + get_tag(record, "<Tag_50>") + ", "
    csvline = csvline + get_tag(record, "<Tag_69>") + ", "
    csvline = csvline + get_tag(record, "<Tag_1>")
    outputfile.write(csvline + "\n")
    return


# input_name  = input("Enter input file name: ")
xmlfile = open("/data/development/winisis_p/KONYV2.xml", encoding="iso-8859-2")
# output_name  = input("Enter output file name: ")
outputfile = open("/data/development/winisis_p/konyvek.csv", "w", encoding="iso-8859-2")
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
        write_record(act_record)
        act_record = list()
xmlfile.close()
