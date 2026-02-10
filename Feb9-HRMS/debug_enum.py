from app import models
print(f"Enum Member: {models.EmploymentType.FullTime}")
print(f"Enum Value: {models.EmploymentType.FullTime.value}")
print(f"Enum Member Type: {type(models.EmploymentType.FullTime)}")
