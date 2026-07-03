with open("resume.txt","w") as file:
    file.write("Name: Aditi\n")
    file.write("College: BIT Patna\n")
    file.write("CGPA: 8.92\n")
with open("resume.txt","r") as file:
    data=file.read()
print(data)
