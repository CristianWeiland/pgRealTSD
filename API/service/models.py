from django.db import models

class Server(models.Model):
    """Server class."""

    POSSIBLE_STATES = (
        ('warmup', 'Warm-Up'),
        ('steady', 'Steady'),
        ('pressure', 'Under Pressure'),
        ('stress', 'Stress'),
        ('thrashing', 'Thrashing')
    )

    name = models.CharField(max_length=128)
    user_name = models.CharField(max_length=128)
    active = models.BooleanField(default=False)
    state = models.CharField(max_length=16, choices=POSSIBLE_STATES, default='warmup')

    def __str__(self):
        return self.name

    def is_valid(self):
        return self.full_clean


class DataList(models.Model):
    """DataList class."""

    POSSIBLE_ATTRIBUTES = (
        ('r', 'Waiting processes'),
        ('b', 'Sleeping processes'),
        ('swpd', 'Virtual memory'),
        ('free', 'Idle memory'),
        ('buff', 'Memory used as buffers'),
        ('cache', 'Memory used as cache'),
        ('inact', 'Inactive memory'),
        ('active', 'Active memory'),
        ('si', 'Memory swapped in'),
        ('so', 'Memory swapped out'),
        ('bi', 'IO (in)'),
        ('bo', 'IO (out)'),
        ('in', 'System interrupts per second'),
        ('cs', 'Context switches per second'),
        ('us', 'CPU User time'),
        ('sy', 'CPU System time'),
        ('id', 'CPU Idle time'),
        ('wa', 'CPU IO wait time'),
        ('st', 'CPU Stolen from a virtual machine time')
    )

    attribute = models.CharField(max_length=8, choices=POSSIBLE_ATTRIBUTES)
    server = models.ForeignKey(Server, related_name='data_list', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('server', 'attribute')


class Data(models.Model):
    """Data class."""

    data_list = models.ForeignKey(DataList, related_name='data', on_delete=models.CASCADE)
    timestamp = models.IntegerField(default=0, db_index=True)
    value = models.IntegerField()

    class Meta:
        unique_together = ('data_list', 'timestamp')
