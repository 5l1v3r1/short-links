import datetime

import short_url

from django.utils import timezone
from django.urls import reverse_lazy
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.core.validators import URLValidator, ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.views.generic.edit import DeleteView
from django.db.models.functions import TruncDay
from django.contrib.auth.decorators import login_required

from .models import Link, Visit


class LinkCreateView(CreateView):
    """
    Create link.
    Supports AJAX and raw form post
    """
    model = Link
    fields = ['origin_link']
    template_name = 'main/index.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        else:
            form.instance.user = None

        try:
            validate = URLValidator(schemes=('http', 'https'))
            validate(form.instance.origin_link)
        except ValidationError:
            form.add_error('origin_link', 'Invalid url!')

        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'short_url': self.request.build_absolute_uri(
                    short_url.encode_url(self.object.pk)
                ),
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class LinkRedirectView(RedirectView):
    """
    Redirect and save click
    """
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        link_id = short_url.decode_url(kwargs['short_link'])
        link = get_object_or_404(Link, pk=link_id)

        # Do not save a click if user is owner, and link has user
        if self.request.user != link.user and link.user is not None:
            visit = Visit(link=link)
            visit.save()
        return link.origin_link


class LinkListView(LoginRequiredMixin, ListView):
    """
    List all link with pagination
    """
    model = Link
    template_name = 'main/link_list.html'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.\
            prefetch_related('visit_set').filter(user=self.request.user)


class LinkDetailView(LoginRequiredMixin, DetailView):
    """
    Detail link
    """
    model = Link
    template_name = 'main/link_detail.html'
    paginate_by = 10

    def get_object(self, queryset=None):
        """ Only for owner """
        link = super().get_object(queryset=queryset)
        if link.user != self.request.user:
            raise Http404()
        return link


class LinkDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deletes link
    """
    model = Link
    template_name = 'main/link_confirm_delete.html'
    success_url = reverse_lazy('main:link-list')


@login_required
def ajax_visits_by_link(request, pk):
    """ Function returns number of clicks for one link in the last 14 days. """
    if request.method == 'GET' and request.is_ajax():
        link = get_object_or_404(Link, pk=pk)
        if request.user != link.user:
            raise Http404()

        time_period = 14

        end_date = timezone.now()
        start_date = end_date - datetime.timedelta(days=time_period)

        queryset = Visit.objects\
            .filter(link=link, datetime__gte=start_date, datetime__lt=end_date)\
            .annotate(date=TruncDay('datetime'))\
            .values('date')\
            .annotate(total=Count('id'))\
            .annotate()\
            .order_by('date')

        items = list(map(lambda x: {'date': x['date'].date(), 'total': x['total']}, queryset))
        dates = [x.get('date') for x in items]

        for d in (end_date.date() - datetime.timedelta(days=x) for x in range(0, time_period)):
            if d not in dates:
                items.append({'date': d, 'total': 0})

        items.sort(key=lambda x: x['date'])

        data = {
            'visits': list(
                map(lambda x: {'date': x['date'].strftime('%m/%d'), 'total': x['total']}, list(items))
            )
        }
        return JsonResponse(data)
    else:
        HttpResponseBadRequest()
