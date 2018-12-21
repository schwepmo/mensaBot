from peewee import Model, SqliteDatabase, CharField, IntegerField, ForeignKeyField, TextField, DateField, BooleanField,\
    FloatField

db = SqliteDatabase("module/sqlite.db")


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    """A person. May be used as a module responsible, reference person, ..."""

    class Meta:
        db_table = "module_person"

    firstname = CharField(max_length=512, unique=True)
    lastname = CharField(max_length=512, unique=True)

    @property
    def fullname(self):
        """Returns the fullname (firstname lastname) from the person"""
        return "{} {}".format(self.firstname, self.lastname)

    def __repr__(self):
        return self.fullname


class Institute(BaseModel):
    """An instititute"""

    class Meta:
        db_table = "module_institute"

    name = CharField(max_length=512, unique=True)
    faculty = CharField(max_length=30)

    def __repr__(self):
        return self.name


class Chair(BaseModel):
    """A chair (Fachgebiet)"""

    class Meta:
        db_table = "module_chair"

    name = CharField()
    chairID = IntegerField(null=True)
    institute = ForeignKeyField(Institute)

    def __repr__(self):
        return self.name


class Program(BaseModel):
    """A study program"""

    class Meta:
        db_table = "module_program"

    name = CharField(max_length=512)
    degree = CharField(max_length=256)

    def __repr__(self):
        return "{} ({})".format(self.name, self.degree)


class CourseRegulation(BaseModel):
    """A course regulation (Studien- und Pruefungsordnung)"""

    class Meta:
        db_table = "module_courseregulation"

    program = ForeignKeyField(Program)
    name = CharField(max_length=512)
    group = CharField(max_length=512)

    def __repr__(self):
        return self.name


class Course(BaseModel):
    """A course (Kurs)"""

    class Meta:
        db_table = "module_course"

    title = CharField(max_length=255, null=False)
    courseType = CharField(null=True, max_length=10)
    courseID = CharField(null=True, max_length=255)
    cycle = CharField(null=True, max_length=10)
    creditHours = IntegerField(null=True)

    courseURL = CharField(null=True, max_length=512)
    content = TextField(null=True)
    annotation = TextField(null=True)
    detailedDescription = TextField(null=True)
    requirements = TextField(null=True)
    literature = TextField(null=True)
    courseAssessment = TextField(null=True)
    teachingContents = TextField(null=True)
    audience = TextField(null=True)
    comment = TextField(null=True)

    def __repr__(self):
        return self.title


class CourseDate(BaseModel):
    class Meta:
        db_table = "module_coursedate"

    course = ForeignKeyField(Course)
    day = CharField(null=True, max_length=10)
    startTime = CharField(null=True, max_length=10)
    endTime = CharField(null=True, max_length=10)
    cycle = CharField(null=True, max_length=10)
    firstDate = CharField(null=True, max_length=20)
    lastDate = CharField(null=True, max_length=20)
    room = CharField(null=True, max_length=256)
    teacher = ForeignKeyField(Person, null=True)
    participantLimitation = IntegerField(null=True)
    comment = CharField(null=True, max_length=256)

    def __repr__(self):
        return "{} ({} - {} bis {})".format(self.course.title, self.day, self.startTime, self.endTime)


class MTSModule(BaseModel):
    """A module extracted from the MTS catalogue"""

    class Meta:
        db_table = "module_mtsmodule"

    id = IntegerField()
    title = CharField(max_length=255, null=True)
    titleEnglish = CharField(max_length=255, null=True)
    ects = IntegerField()
    moduleID = IntegerField()
    version = IntegerField()
    effective = DateField()
    validity = CharField(max_length=100)
    lang = CharField(max_length=10)
    chair = ForeignKeyField(Chair, null=True)
    responsiblePerson = ForeignKeyField(Person, null=True)
    mailAddress = CharField(null=True, max_length=255)
    website = CharField(null=True, max_length=512)
    referencePerson = ForeignKeyField(Person, null=True)
    administrationOffice = CharField(null=True, max_length=100)
    learningOutcomes = TextField(null=True)
    learningOutcomesEnglish = TextField(null=True)
    teachingContents = TextField(null=True)
    teachingContentsEnglish = TextField(null=True)

    url = CharField(max_length=512, unique=True)

    # courses = ManyToManyField(Course)

    instructiveForm = TextField()

    optionalRequirements = TextField()
    mandatoryRequirements = TextField(null=True)

    graded = BooleanField(default=True)
    typeOfExamination = CharField(max_length=1)

    examinationDescription = TextField(null=True)

    numberOfTerms = IntegerField(null=False)

    participantLimitation = IntegerField(null=True)

    registrationFormalities = TextField(null=True)
    miscellaneous = TextField(null=True)

    script = BooleanField(default=False)
    scriptElectronic = BooleanField(default=False)

    literature = TextField(null=False)

    # courseRegulations = ManyToManyField(CourseRegulation)

    def __repr__(self):
        return self.title


class MTSModuleCourses(BaseModel):
    class Meta:
        db_table = "module_mtsmodule_courses"

    mtsmodule = ForeignKeyField(MTSModule, backref="courses")
    course = ForeignKeyField(Course, backref="modules")


class MTSModuleCourseRegulations(BaseModel):
    class Meta:
        db_table = "module_mtsmodule_courseRegulations"

    mtsmodule = ForeignKeyField(MTSModule, backref="courseregulations")
    courseregulation = ForeignKeyField(CourseRegulation, backref="modules")


class ExamElement(BaseModel):
    description = CharField(max_length=512, null=False)
    points = IntegerField()
    module = ForeignKeyField(MTSModule)

    class Meta:
        db_table = "module_examelement"

    def __repr__(self):
        return "{} ({:d} Punkte)".format(self.description, self.points)


class WorkingEffort(BaseModel):
    description = CharField(max_length=512, null=False)
    category = CharField(max_length=512, null=False)

    class Meta:
        db_table = "module_workingeffort"

    multiplier = FloatField()
    hours = FloatField()
    total = FloatField()

    module = ForeignKeyField(MTSModule, null=True)

    def __repr__(self):
        return "{} ({:d} Stunden)".format(self.description, self.total)
