from rest_framework import serializers
from first_app.models import Course
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields ="__all__"


# from rest_framework import serializers

# class NameSerializer(serializers.Serializer):
#     def multiples_of_1000(value):
#         if value % 1000 != 0:
#             raise serializers.ValidationError('Salary should be multiples of 1000s')

#     def validate_esal(self,value):
#         if value>5000:
#             raise serializers.ValidationError('Employee Salary cannot be greater that 5000')
#         return value

#     def validate(self,data):
#         pwd = data.get('pwd')
#         cnf_pwd = data.get('cnf_pwd')
#         if pwd!=cnf_pwd:
#             raise serializers.ValidationError("Both password and pwd must be Same")
#         return data

#     esal=serializers.IntegerField(validators=[multiples_of_1000])

#     pwd=serializers.CharField()
#     cnf_pwd=serializers.CharField()

#     name=serializers.CharField(max_length=7)


    

