import sys

def update():
    student = [[]]
    f = open('student-data/id.txt','r')

    x = f.readline()
    i = 0
    while x != 'end':
        student[i].append(x)
        x = f.readline()

    for r in student:
        print r
    
if __name__ == '__main__':
    update()


