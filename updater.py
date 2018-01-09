import sys
from django.db import connection, transaction
from profiles.models import *

def update(filename):
    cursor = connection.cursor()
    f = open(filename,'r')

    update = 0
    create = 0
    x = f.readline()

    while x != 'end':
        try:
            templst = x.split(',')
            try:
                student = Student.objects.get(studentID=int(templst[0]))
                if student is not None:
                    student.lastname = templst[1]
                    student.firstname = templst[2]
                    student.gender = templst[3]
                    student.school = templst[4]
                    student.year = int(templst[5])
                    student.save()
                    print "Updated: ", student
                    update += 1
            except Student.DoesNotExist as e:
                dup = Student.objects.filter(lastname=templst[1],firstname=templst[2],gender=templst[3],school=templst[4],year=templst[5])
                if len(dup) == 0:
                    student = Student.objects.create(studentID=templst[0],lastname=templst[1],firstname=templst[2],gender=templst[3],school=templst[4],year=templst[5])
                    print "Created: ", student
                    student.save()
                    create += 1
            except Exception as e:
                print e, "Exception"
        except Exception as e:
            print e 

        x = f.readline()
    print "end: create: ", int(create) ," , update: ", int(update)
if __name__ == '__main__':
    update()


