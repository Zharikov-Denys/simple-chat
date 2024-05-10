from django.db.models import QuerySet


class ThreadQuerySet(QuerySet):
    def prefetch_participants(self):
        return self.prefetch_related('participants')
