from rest_framework import serializers
from first_app.models import Course
from first_app.models import Employee, Teachers, Student
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields ="__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields='__all__'
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'


class CourseNoRequiredSerializer(serializers.ModelSerializer):
    """
        This serializer is created just for swagger response purpose.
    """
    
    def __init__(self, *args, **kwargs):
        '''
          For setting all fields required attribute to False for swagger response use only
        '''
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False

    class Meta:
        model=Course
        fields='__all__'
        ref_name = "Response Data"  # for overriding model value on swagger ui


class TeachersSerializer(serializers.Serializer):

    def multiples_of_1000(value):
        if value % 1000 != 0:
            raise serializers.ValidationError('Salary should be multiples of 1000s')

    def validate_teacher_sal(self,value):
        if value>5000:
            raise serializers.ValidationError('Employee Salary cannot be greater that 5000')
        return value

    def validate(self,data):
        pwd = data.get('teacher_addr')
        if pwd=="":
            raise serializers.ValidationError("Both password and pwd must be Same")
        return data
    
    id = serializers.IntegerField(read_only=True)
    teacher_name=serializers.CharField(max_length=27)
    teacher_sal=serializers.FloatField(validators=[multiples_of_1000])
    teacher_addr=serializers.CharField()
            
    def create(self, validated_data):
        """
        Create and return a new instance of the validated data.
        """
        return Teachers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing instance with the validated data.
        """
        instance.teacher_name = validated_data.get('teacher_name', instance.teacher_name)
        instance.teacher_sal = validated_data.get('teacher_sal', instance.teacher_sal)
        instance.teacher_addr = validated_data.get('teacher_addr', instance.teacher_addr)
        instance.save()
        return instance

class TeachersNoRequiredSerializer(serializers.Serializer):
    """
        This serializer is created just for swagger response purpose.
    """
    
    def __init__(self, *args, **kwargs):
        '''
          For setting all fields required attribute to False for swagger response use only
        '''
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False

    id = serializers.IntegerField(read_only=True)
    teacher_name=serializers.CharField(max_length=27)
    teacher_sal=serializers.FloatField()
    teacher_addr=serializers.CharField()
     
    class Meta:
        ref_name = ""  # for overriding model value on swagger ui
       
    def create(self, validated_data):
        """
        Create and return a new instance of the validated data.
        """
        return Teachers.objects.create(**validated_data)


    

