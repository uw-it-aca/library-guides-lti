from django.db import models
from sis_provisioner.models import Curriculum


class Library(models.Model):
    """ Represents a library.
    """
    name = models.CharField(max_length=512, null=True)
    description = models.CharField(max_length=8192, null=True)
    url = models.CharField(max_length=512, null=True)


class Librarian(models.Model):
    """ Represents a librarian.
    """
    name = models.CharField(max_length=512, null=True)
    email = models.CharField(max_length=512, null=True)
    phone = models.CharField(max_length=512, null=True)
    url = models.CharField(max_length=512, null=True)


class SubjectGuide(models.Model):
    """ Represents a subject guide.
    """
    library = models.ForeignKey(Library,
                                related_name="+",
                                  null=True,
                                on_delete=models.PROTECT)
    librarian = models.ForeignKey(Librarian,
                                  related_name="+",
                                  null=True,
                                  on_delete=models.PROTECT)
    name = models.CharField(max_length=512, null=True)
    label = models.CharField(max_length=1024, null=True)
    url = models.CharField(max_length=512, null=True)


class CurriculumGuide(models.Model):
    """ Links subject guides to curricula.
    """
    curriculum = models.ForeignKey(Curriculum,
                                   related_name="+",
                                   on_delete=models.PROTECT)
    subject_guide = models.ForeignKey(SubjectGuide,
                                      related_name="+",
                                      on_delete=models.PROTECT)
