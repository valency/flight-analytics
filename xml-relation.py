import getopt
import sys
from xml.etree import ElementTree


def main(argv):
    usage = 'xml-relation.py -t <table,e.g.,HISTORYFLIGHT> -f <file,e.g.,data>'
    data_table = "HISTORYFLIGHT"
    data_file_name = "AFOCDB_Oracle.pdm"
    try:
        opts, args = getopt.getopt(argv, "ht:f:")
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        elif opt == '-t':
            table = arg
        elif opt == '-f':
            data_file_name = arg
    # log("Table = " + data_table)
    # log("Data File = " + data_file_name)
    with open(data_file_name, 'r') as f:
        root = ElementTree.fromstring(f.read()).getchildren()[0].getchildren()[0].getchildren()[0]
    tables = root.find("{collection}Tables").getchildren()
    references = root.find("{collection}References").getchildren()
    foreign_keys = []
    for reference in references:
        for reference_join in reference.find("{collection}Joins").getchildren():
            foreign_keys.append((reference_join.find("{collection}Object1").find("{object}Column").get("Ref"), reference_join.find("{collection}Object2").find("{object}Column").get("Ref")))
    column_collection = []
    target_foreign_keys = []
    for table in tables:
        columns = table.find("{collection}Columns")
        if columns is not None:
            for column in columns:
                column_id = column.get("Id")
                column_name = column.find("{attribute}Name").text
                column_collection.append({
                    "id": column_id,
                    "name": column_name,
                    "table": {
                        "id": table.get("Id"),
                        "name": table.find("{attribute}Name").text
                    }
                })
                if table.find("{attribute}Name").text == data_table:
                    for key_pair in foreign_keys:
                        if column_id == key_pair[1]:
                            target_foreign_keys.append({
                                "id": column_id,
                                "name": column_name,
                                "fkid": key_pair[0]
                            })
    flag = False
    for key in target_foreign_keys:
        if flag:
            print "AND"
        else:
            flag = True
        print key["name"], "=",
        for column in column_collection:
            if key["fkid"] == column["id"]:
                print column["table"]["name"] + "." + column["name"],
    print


if __name__ == "__main__":
    main(sys.argv[1:])
