import sys
import argparse

from datetime import datetime, timezone

from stampchecker.Controller import Controller

def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", type=str, required=True, help="Path to TSK body file")
    args = parser.parse_args()

    c = Controller()
    c.printHeader(args.path)

    with open(args.path, "r", encoding="utf-8") as f:

        while True:
            line = f.readline()

            if not line:
                break
            
            line = line.replace("\n", "")
            splittedLine = line.split("|")

            atime = int(splittedLine[7])
            mtime = int(splittedLine[8])
            ctime = int(splittedLine[9])
            crtime = int(splittedLine[10])

            if(crtime > mtime or crtime > atime or crtime > ctime):
                print("")
                print("              ---> " + splittedLine[1])
                print("-------------------")
                print("    Creation Time: " + str(datetime.fromtimestamp(crtime, tz=timezone.utc)) + " - " + str(crtime))
                print("-------------------")
                if(crtime > atime and atime > 0):
                    print("    Accessed Time: " + str(datetime.fromtimestamp(atime, tz=timezone.utc)) + " - " + str(atime))
                if(crtime > mtime and mtime > 0):
                    print("Modification Time: " + str(datetime.fromtimestamp(mtime, tz=timezone.utc)) + " - " + str(mtime))
                if(crtime > ctime and ctime > 0):
                    print("     Changed Time: " + str(datetime.fromtimestamp(ctime, tz=timezone.utc)) + " - " + str(ctime))
                print("-------------------")
                print("")

    c.printExecutionTime()

if __name__ == "__main__":
    sys.exit(main())
