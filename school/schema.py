# schema.py

import graphene
from graphene_django.types import DjangoObjectType
from .models import Student, Teacher, Course

class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        field = '__all__'

class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher
        field = '__all__'

class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        field = '__all__'

class CreateStudent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        age = graphene.Int()

    # outputs fields
    student = graphene.Field(lambda: StudentType)

    def mutate(self, info, name, age):
        student = Student(name=name, age=age)
        student.save()
        return CreateStudent(student=student)

class UpdateStudent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        age = graphene.Int()

    # outputs fields
    student = graphene.Field(lambda: StudentType)

    def mutate(elf, info, id, name, age):
        student = Student.objects.get(id=id)
        if name:
            student.name = name
        if age:
            student.age = age
        student.save()
        return UpdateStudent(student=student)

class DeleteStudent(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        try:
            student = Student.objects.get(id = id)
            student.delete()
            return DeleteStudent(ok = True)
        except:
            return DeleteStudent(ok = False)
        
class Query(graphene.ObjectType):
    all_students = graphene.List(StudentType)
    all_teachers = graphene.List(TeacherType)
    all_courses = graphene.List(CourseType)

    def resolve_all_students(self, info):
        return Student.objects.all()

    def resolve_all_teachers(self, info):
        return Teacher.objects.all()

    def resolve_all_courses(self, info):
        return Course.objects.all()

class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    update_student = UpdateStudent.Field()
    delete_student = DeleteStudent.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)