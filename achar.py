
def SaveData(data,path="JarvisAI//chat.log"):
    with open(path,"w") as f:
        if type(data) == str:
            f.write(f'"""{data}"""')
        else:
            f.write(str(data))
    return True

def LoadData(path = "JarvisAI//chat.log"):
    try:
        with open(path,"r") as f:
            data = eval(f.read())
        return data 
    except FileNotFoundError:
        SaveData([],path)
        return []
    except:
        return LoadData(path=path)
    
# SaveData("hello world")
# print(LoadData())
# print(type(LoadData()))