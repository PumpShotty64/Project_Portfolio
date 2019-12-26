from pathlib import Path
import shutil
import os

def search_directories(com, folder, fileList):

    p = Path(folder)
    sublst = []

    try:
        if com == "D" and p.exists():
            for x in p.iterdir():
                if x.is_file():
                    print(x)
                    fileList.append(x)
        elif com == "R" and p.exists():
            for x in p.iterdir():
                if x.is_file():
                    print(x)
                    fileList.append(x)
                elif x.is_dir():
                    sublst.append(x)

            for i in sublst:
                search_directories(com, i, fileList)
        else:
            print("ERROR")
            reCom, reDir = input().split(" ", 1)
            search_directories(reCom, reDir, fileList)
    except OSError:
        print("ERROR")
        reCom, reDir = input().split(" ", 1)
        search_directories(reCom, reDir, fileList)

    return fileList


def file_commands(fileList, outputList):

    fileCommand = input()

    if fileCommand == "A":
        for file in fileList:
            print(file)
            outputList.append(file)

    elif fileCommand != "A":

        try:
            com, obj = fileCommand.split(" ", 1)

            if com == "N":
                for file in fileList:
                    if obj == file.name:
                        print(file)
                        outputList.append(file)

            elif com == "E":
                for file in fileList:
                    if "." in obj:
                        obj = obj[1:]

                    obj = "." + obj

                    if obj == file.suffix:
                        print(file)
                        outputList.append(file)

            elif com == "T":
                for file in fileList:
                    if file.suffix == ".txt":
                        tempFile = open(file, "r").read()
                        if obj in tempFile:
                            print(file)
                            outputList.append(file)

            elif com == "<":
                for file in fileList:
                    if file.stat().st_size < int(obj):
                        print(file)
                        outputList.append(file)

            elif com == ">":
                for file in fileList:
                    if file.stat().st_size > int(obj):
                        print(file)
                        outputList.append(file)
            else:
                print("ERROR")
                file_commands(fileList, outputList)

            if not outputList:
                return None

        except ValueError:
            print("ERROR")
            file_commands(fileList, outputList)
    else:
        print("ERROR")
        file_commands(fileList, outputList)

    return outputList


def final_command(fileList):

    finalCommand = input()

    if finalCommand == "F":

        for file in fileList:

            if file.suffix == ".txt":
                try:
                    tempFile = open(file, "r")
                    tempList = [line[:-1] for line in tempFile]
                    print(tempList[0])
                except IndexError:
                    print("")
            else:
                print("NOT TEXT")

    elif finalCommand == "D":
        tempPath = os.getcwd()
        os.mkdir("temp")
        for file in fileList:
            p = Path(shutil.copy2(file, (tempPath + "/temp")))
            p.rename(Path(p.parent, p.name + ".dup"))
            newPath = p.parent / (p.name + ".dup")
            shutil.move(os.fspath(newPath), file.parent)
        os.rmdir("temp")

    elif finalCommand == "T":
        for file in fileList:
            Path.touch(file)

    else:
        print("ERROR")
        final_command(fileList)

if __name__ == '__main__':

    isRun = True
    while isRun:
        try:
            interestingList = []
            finalList = []
            command, directory = input().split(" ", 1)

            interestingList = search_directories(command, directory, interestingList)
            finalList = file_commands(interestingList, finalList)
            if finalList is not None:
                final_command(finalList)
                isRun = False
            else:
                break

        except ValueError:
            print("ERROR")
