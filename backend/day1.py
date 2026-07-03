class Resume:
    def __init__(self,name,college,cgpa,skills):
        self.name=name
        self.college=college
        self.cgpa=cgpa
        self.skills=skills
    def display(self):
        print(f"Name: {self.name}")
        print(f"College : {self.college}")
        print(f"CGPA : {self.cgpa}")
        print("Skills: ")
        for skill in self.skills:
            print(f"    -{skill}")
s1=Resume("Aditi","BIT Patna",8.92,["ML","Python","Gen AI","LLM"])
s1.display()
