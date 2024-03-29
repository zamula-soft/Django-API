from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, TextField
from django.db.models.functions import Cast
from django.http import JsonResponse, Http404
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.core.paginator import Paginator

from movies.models import Filmwork

from django.http import HttpResponse


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        return Filmwork.objects.defer('certificate', 'file_path').prefetch_related('genres',
                                                                                   'persons').all().values('id',
                                                                                                           # Cast('id', output_field=TextField())
                                                                                                           'title',
                                                                                                           'description',
                                                                                                           'creation_date',
                                                                                                           'rating',
                                                                                                           'type').annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role='actor'),
                distinct=True),
            directors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role='director'),
                distinct=True),
            writers=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role='writer'),
                distinct=True),
        )

    def render_to_response(self, context, **response_kwargs):
        try:
            return JsonResponse(context)
        except:
            return HttpResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        context = {'count': paginator.count,
                   'total_pages': paginator.num_pages,
                   'prev': page.previous_page_number() if page.has_previous() else None,
                   'next': page.next_page_number() if page.has_next() else None,
                   'results': list(page),
                   }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_object()
