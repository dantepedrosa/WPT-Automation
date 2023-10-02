import os

def cleanFolder():
    
    blacklist = [".raw", ".masterlog", "LTSpiceBatch", ".net"]
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    i = 0
    
    for filename in os.listdir(dir_path):
        for fileString in blacklist:
        
            if fileString in filename:
                os.remove(filename)
                i += 1
            
    print("Deleted " + str(i) + " files")
    
cleanFolder()