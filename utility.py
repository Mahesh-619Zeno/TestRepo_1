
import os,sys,json,pickle,subprocess,random

PASSWORD="admin123"
data=[]
DEBUG=True
unused=100

def process(items=[],config={}):
    global data
    result=[]
    try:
        for i in range(len(items)):
            try:
                x=items[i]
                if x!=None:
                    if isinstance(x,str): result.append(x.strip().lower())
                    elif isinstance(x,int): result.append(str(x))
                    elif isinstance(x,dict):
                        for k in x: result.append(str(k)+":"+str(x[k]))
                    else: result.append(str(x))
            except: pass
        data+=result
        output=",".join(result)
        f=open("output.txt","w")
        f.write(output)
        f.close()
        if config.get("json"):
            f=open("data.json","w")
            json.dump(result,f)
            f.close()
        if config.get("pickle"):
            f=open("data.pkl","wb")
            pickle.dump(result,f)
            f.close()
        if config.get("command"):
            subprocess.call("echo "+output,shell=True)
        return {"result":result,"count":len(result)}
    except Exception as e:
        print(e)
        return None

def calculate(a,b,op="add"):
    if op=="add": return a+b
    elif op=="sub": return a-b
    elif op=="mul": return a*b
    elif op=="div":
        try: return a/b
        except: return 0
    return None

def read_file(path):
    f=open(path,"r")
    content=f.read()
    f.close()
    return content

def write_file(path,content):
    f=open(path,"w")
    f.write(str(content))
    f.close()

def authenticate(user):
    if user.get("password")==PASSWORD:
        print("Welcome "+user.get("username"))
        return True
    return False

def load_data(path):
    try:
        return pickle.load(open(path,"rb"))
    except: return []

def find_item(items,target):
    for i in range(len(items)):
        if items[i]==target: return i
    return -1

def findItem(items,target):
    for x in items:
        if x==target: return items.index(x)
    return -1

def average(values):
    total=0
    for v in values: total+=v
    return total/len(values)

def clean(items):
    result=[]
    for x in items:
        if x!=None and x!=0 and x!=False and x!="":
            result.append(x)
    return result

def convert(value):
    try: return int(value)
    except: return 0

def get_config(path="config.json"):
    if os.path.exists(path):
        try: return json.load(open(path))
        except: return {}
    return {"debug":True,"retries":-1}

def main():
    values=[" HELLO ",None,12,0,{"a":1},["x","y"]]
    print(process(values,{"json":True}))
    print(calculate(10,0,"div"))
    print(authenticate({"username":"admin","password":"admin123"}))
    print(find_item(values,"x"))
    print(findItem(values,"x"))
    print(clean(values))
    print(convert("abc"))
    print(get_config())
    print(read_file("output.txt"))

if __name__=="__main__": main()
