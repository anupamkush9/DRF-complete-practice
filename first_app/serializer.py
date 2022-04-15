from rest_framework import serializers

class NameSerializer(serializers.Serializer):
    # def multiples_of_1000(value):
    #     if value % 1000 != 0:
    #         raise serializers.ValidationError('Salary should be multiples of 1000s')

    # def validate_esal(self,value):
    #     if value>5000:
    #         raise serializers.ValidationError('Employee Salary cannot be greater that 5000')
    #     return value
    def validate(self,data):
        esal = data.get('esal')
        if esal==10000:
            raise serializers.ValidationError("salary cannot be 10 thousand")
        return data

    esal=serializers.IntegerField(validators=[])

    pwd=serializers.CharField()
    cnf_pwd=serializers.CharField()

    name=serializers.CharField(max_length=7)
    # esal=serializers.IntegerField()


    

