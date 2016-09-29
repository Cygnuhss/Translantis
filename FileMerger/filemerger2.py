import sys
import os
import getopt

OPTIONS = ["TOPIC", "YEAR"]


def merge(root, option, values, extension="txt"):
    """Merge all files in nested subfolders based on an option (topic or year),
    where all files containing the search term are piled in a single file in the
    root folder.
    """
    if option.upper() not in OPTIONS:
        raise ValueError("Options is not implemented: {}".format(option))
    elif option.upper() == "TOPIC":
        searchTerms = values
    elif option.upper() == "YEAR":
        startYear, endYear = values
        searchTerms = range(startYear, endYear+1)
    else:
        raise ValueError("Update merge OPTIONS, option is not included: {}".format(option))

    for searchTerm in searchTerms:
        document = mergeSimilarDocuments(root, searchTerm)

        filename = '{}.{}'.format(str(searchTerm), str(extension))
        with open(filename, 'w+') as f:
            f.write(document)

def mergeSimilarDocuments(root, searchTerm):
    """Retrieve and merge all documents in nested subfolders that contain the
    search term in the filename.
    """
    searchTerm = str(searchTerm).lower()

    document = []
    for root, directories, files in os.walk(root):
        for name in files:
            filepath = os.path.join(root, name)
            print(filepath)
            if searchTerm in filepath.lower():
                with open(filepath, 'r') as f:
                    document.append(f.read())

    print(''.join(document))
    return ''.join(document)


def main(argv):
    """Find all files in nested folders starting from a root that contain the
    same search term and combine them into a single file.

    Usage:
        filemerger.py -r <root> -o <option> -v <values>
    where <root> is specified path to the starting folder,
    <option> is a search option, either TOPIC or YEAR, and
    <values> is a comma-separated string of values.
    A valid example is:
        filemerger.py -r ./test -o topic -v="test1,test2"
    Or by year (only two values are allowed: the start and end year):
        filemerger.py -r ./test -o year -v="1990,2000"
    """
    try:
        opts, args = getopt.getopt(argv,"hr:o:v:",["root=","option=","values="])
    except getopt.GetoptError:
        print('filemerger.py -r <root> -o <option> -v <values>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('filemerger.py -r <root> -o <option> -v <values>')
            sys.exit()
        elif opt in ("-r", "--root"):
            root = arg
        elif opt in ("-o", "--option"):
            option = arg
        elif opt in ("-v", "--values"):
            values = arg.split(',')

    if option.upper() == "YEAR":
        values = [int(x) for x in values]

    merge(root, option, values)

    print("Done: Files merged by {} in root {}.".format(option, root))


if __name__ == "__main__":
    main(sys.argv[1:])
