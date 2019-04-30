import subprocess

if __name__=="__main__":
    out = subprocess.Popen(["wsk", "-i", "action", "list"], stdout=subprocess.PIPE)
    result = str(out.communicate()).split(' ')
    for substring in result:
        try:
            index_start = substring.index('/guest')
            out2 = subprocess.Popen(["wsk", "-i", "action", "delete", substring[index_start + 7:]], stdout=subprocess.PIPE)
        except ValueError:
            pass
