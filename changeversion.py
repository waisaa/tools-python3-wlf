def change_version():
    file = 'setup.py'
    prefix = 'VNU'
    file_data = ""
    with open(file, "r", encoding="utf-8") as fr:
        for line in fr:
            if line.startswith(prefix):
                vnu = int(line.split('=')[1]) + 1
                line = "{} = {}\n".format(prefix, vnu)
            file_data += line
    with open(file, "w", encoding="utf-8") as fw:
        fw.write(file_data)


def main():
    change_version()


if __name__ == '__main__':
    main()
