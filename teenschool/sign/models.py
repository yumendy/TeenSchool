from django.db import models

# Create your models here.
class Project(models.Model):

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50)
    startTime = models.DateTimeField(null=True)
    signinTime = models.DateTimeField(null=True)
    signoutTime = models.DateTimeField(null=True)

class Record(models.Model):

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __unicode__(self):
        return self.name
    
    num = models.CharField(max_length=11)
    name = models.CharField(null=True, max_length=50)
    typ = models.IntegerField()
    signTime = models.DateTimeField()
    signIp = models.IPAddressField()
    project = models.ForeignKey(Project)