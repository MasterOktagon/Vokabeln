
import json

def load_set(path: str)->dict:
    with open(path, "r") as f:
        data = json.loads(f.read())
        return data
        
        
def save_set(path: str, data: dict)->None:
    with open(path, "w") as f:
        f.write(json.dumps(data))




# Test code
if __name__ == "__main__":
    save_set("test.json", {"Farbe":"Coleur"})
    print(load_set("test.json")["Farbe"])




