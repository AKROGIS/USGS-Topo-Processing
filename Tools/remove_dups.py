import os

pdf_folder = "B:/work/topo"
status_file = "C:/tmp/topo/status.txt"

with open(status_file) as filelist:
    for line in filelist:
        #print(line)
        if line.startswith("dup:"):
            #print(line)
            filename = line.replace("dup:", "").strip()
            filepath = os.path.join(pdf_folder, filename)
            try:
                os.remove(filepath)
                print("deleted {0}".format(filepath))
            except Exception as ex:
                print(ex)
