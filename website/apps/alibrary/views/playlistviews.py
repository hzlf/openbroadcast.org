# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from elasticsearch_dsl import TermsFacet, RangeFacet

from search.views import BaseFacetedSearch, BaseSearchListView

from ..forms import PlaylistForm, ActionForm
from ..models import Playlist
from ..documents import PlaylistDocument

log = logging.getLogger(__name__)


class PlaylistSearch(BaseFacetedSearch):
    doc_types = [PlaylistDocument]
    fields = ['tags', 'name', ]

    facets = {
        'tags': TermsFacet(field='tags', size=100),
        'type': TermsFacet(field='type', size=100, order={'_key': 'asc'}),
        'status': TermsFacet(field='status', size=100, order={'_key': 'asc'}),
        'weather': TermsFacet(field='weather', size=100, order={'_key': 'asc'}),
        'seasons': TermsFacet(field='seasons', size=100, order={'_key': 'asc'}),
        'daypart_days': TermsFacet(field='daypart_days', size=100),
        'daypart_slots': TermsFacet(field='daypart_slots', size=100, order={'_key': 'asc'}),
        'target_duration': TermsFacet(field='target_duration', size=100),
        #'num_emissions': TermsFacet(field='num_emissions', size=100),
        'num_emissions': RangeFacet(field='num_emissions', ranges=[
            ('None', (0, 1)),
            ('1 - 10', (1, 10)),
            ('11 - 50', (11, 50)),
            ('More than 50', (50, None)),
        ]),
    }


class PlaylistListView(BaseSearchListView):
    model = Playlist
    template_name = 'alibrary/playlist_list_ng.html'
    search_class = PlaylistSearch
    scope = 'public'
    order_by = [
        {
            'key': 'name',
            'name': _('Name'),
            'default_direction': 'asc',
        },
        {
            'key': 'num_emissions',
            'name': _('Num Emissions'),
            'default_direction': 'desc',
        },
        {
            'key': 'duration',
            'name': _('Duration'),
            'default_direction': 'asc',
        },
        {
            'key': 'updated',
            'name': _('Last modified'),
            'default_direction': 'desc',
        },
        {
            'key': 'created',
            'name': _('Creation date'),
            'default_direction': 'desc',
        },
    ]

    def get_search_query(self, **kwargs):
        serach_query = super(PlaylistListView, self).get_search_query(**kwargs)

        if self.scope == 'own':
            serach_query['searches'].update({
                'user': [
                    self.request.user.username,
                ],
            })
        else:
            serach_query['searches'].update({
                'type': [
                    '-Private Playlist',
                ],
            })

        # print(serach_query)

        return serach_query

    def get_queryset(self, **kwargs):
        qs = super(PlaylistListView, self).get_queryset(**kwargs)

        qs = qs.select_related(
            'series',
            'user',
            'user__profile',
        ).prefetch_related(
            'items',
            'dayparts',
            'seasons',
            'weather',
        )

        # TODO: refactor enumerations
        if not self.scope == 'own':
            qs = qs.exclude(type='basket')

        return qs


# class PlaylistListView(PaginationMixin, ListView):
#
#     context_object_name = "playlist_list"
#     template_name = "alibrary/playlist_list.html"
#
#     paginate_by = ALIBRARY_PAGINATE_BY_DEFAULT
#     extra_context = {}
#
#     def get_paginate_by(self, queryset):
#
#         ipp = self.request.GET.get('ipp', None)
#         if ipp:
#             try:
#                 if int(ipp) in ALIBRARY_PAGINATE_BY:
#                     return int(ipp)
#             except Exception as e:
#                 pass
#
#         return self.paginate_by
#
#     def get_context_data(self, **kwargs):
#
#
#         context = super(PlaylistListView, self).get_context_data(**kwargs)
#
#
#         self.extra_context['filter'] = self.filter
#         self.extra_context['relation_filter'] = self.relation_filter
#         self.extra_context['tagcloud'] = self.tagcloud
#         # for the ordering-box
#         self.extra_context['order_by'] = ORDER_BY
#
#         # active tags
#         if self.request.GET.get('tags', None):
#             tag_ids = []
#             for tag_id in self.request.GET['tags'].split(','):
#                 tag_ids.append(int(tag_id))
#             self.extra_context['active_tags'] = tag_ids
#
#         self.extra_context['list_style'] = self.request.GET.get('list_style', 'l')
#         self.extra_context['get'] = self.request.GET
#
#         context.update(self.extra_context)
#
#         return context
#
#
#     def get_queryset(self, **kwargs):
#
#
#         self.tagcloud = None
#         q = self.request.GET.get('q', None)
#
#         #qs = Playlist.objects.all()
#
#         if self.request.user.is_authenticated():
#             qs = Playlist.objects.filter(~Q(type='basket') | Q(user__pk=self.request.user.pk))
#         else:
#             qs = Playlist.objects.exclude(type='basket')
#
#         if q:
#             # haystack version
#             #sqs = SearchQuerySet().models(Playlist).filter(SQ(content__contains=q) | SQ(content_auto=q))
#             #sqs = SearchQuerySet().models(Playlist).filter(content=AutoQuery(q))
#             sqs = SearchQuerySet().models(Playlist).filter(text_auto=AutoQuery(q))
#             qs = qs.filter(id__in=[result.object.pk for result in sqs]).distinct()
#
#             # ORM version
#             # qs = qs.filter(Q(name__icontains=q)\
#             # | Q(series__name__icontains=q)\
#             # | Q(user__username__istartswith=q))\
#             # .distinct()
#
#         order_by = self.request.GET.get('order_by', None)
#         direction = self.request.GET.get('direction', None)
#
#         if order_by and direction:
#             if direction == 'descending':
#                 qs = qs.order_by('-%s' % order_by)
#             else:
#                 qs = qs.order_by('%s' % order_by)
#
#
#
#         if 'type' in self.kwargs:
#             qs = qs.filter(type=self.kwargs['type'])
#
#         if 'user' in self.kwargs:
#             user = get_object_or_404(User, username=self.kwargs['user'])
#             if 'type' in self.kwargs:
#                 qs = qs.filter(type=self.kwargs['type'], user=user)
#             else:
#                  qs = qs.filter(type__in=['playlist', 'broadcast', 'basket'],user=user)
#
#         # special relation filters
#         self.relation_filter = []
#
#         user_filter = self.request.GET.get('user', None)
#         if user_filter:
#             user = get_object_or_404(User, username=user_filter)
#             #qs = qs.filter(media_release__artist__slug=artist_filter).distinct()
#             # incl album_artists
#             qs = qs.filter(user=user).distinct()
#
#             # add relation filter
#             fa = user # for consistency
#             f = {'item_type': 'user' , 'item': fa, 'label': _('User')}
#             self.relation_filter.append(f)
#
#
#         # apply filters
#         self.filter = PlaylistFilter(self.request.GET, queryset=qs)
#         qs = self.filter.qs
#
#         archived_filter = self.request.GET.get('archived_filter', None)
#         if archived_filter:
#
#             if archived_filter == 'yes':
#                 qs = qs.filter(
#                     rotation_date_end__lt=timezone.now().date()
#                 ).distinct()
#
#             if archived_filter == 'no':
#                 qs = qs.exclude(
#                     rotation_date_end__lt=timezone.now().date()
#                 ).distinct()
#
#
#
#
#         stags = self.request.GET.get('tags', None)
#         tstags = []
#         if stags:
#             stags = stags.split(',')
#             for stag in stags:
#                 tstags.append(int(stag))
#
#         if stags:
#             qs = Release.tagged.with_all(tstags, qs)
#
#
#         # rebuild filter after applying tags
#         self.filter = PlaylistFilter(self.request.GET, queryset=qs)
#
#
#         # tagging / cloud generation
#         if qs.exists():
#             tagcloud = Tag.objects.usage_for_queryset(qs, counts=True, min_count=0)
#             self.tagcloud = calculate_cloud(tagcloud)
#
#         return qs
#
#     """
#     def get_queryset(self):
#         kwargs = {}
#         return Playlist.objects.filter(**kwargs)
#     """

class PlaylistDetailView(DetailView):
    context_object_name = "playlist"
    model = Playlist

    def render_to_response(self, context):
        return super(PlaylistDetailView, self).render_to_response(context, content_type="text/html")

    def get_context_data(self, **kwargs):
        context = super(PlaylistDetailView, self).get_context_data(**kwargs)
        return context


class PlaylistCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Playlist

    template_name = 'alibrary/playlist_create.html'
    form_class = PlaylistForm

    permission_required = 'alibrary.add_playlist'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(PlaylistCreateView, self).get_context_data(**kwargs)
        context['action_form'] = ActionForm()
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_edit_url())


class PlaylistDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Playlist
    template_name = 'alibrary/playlist_delete.html'
    permission_required = 'alibrary.delete_playlist'
    raise_exception = True

    # TODO: this is a hack/bug/issue
    # http://stackoverflow.com/questions/7039839/how-do-i-use-reverse-or-an-equivalent-to-refer-to-urls-that-are-hooked-into-dj
    success_url = reverse_lazy('alibrary-playlist-list')

    def dispatch(self, request, *args, **kwargs):

        # TODO: here we could implement permission check for 'shared-editing' playlists
        obj = Playlist.objects.get(pk=int(kwargs['pk']))
        if not obj.user == request.user:
            raise PermissionDenied

        # check if possible to delete
        can_delete, reason = obj.can_be_deleted()
        if not can_delete:
            messages.add_message(request, messages.ERROR, reason)
            return HttpResponseRedirect(obj.get_edit_url())

        return super(PlaylistDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlaylistDeleteView, self).get_context_data(**kwargs)

        return context


class PlaylistEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Playlist
    template_name = "alibrary/playlist_edit.html"
    success_url = '#'
    form_class = PlaylistForm

    permission_required = 'alibrary.change_playlist'
    raise_exception = True

    def __init__(self, *args, **kwargs):
        super(PlaylistEditView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):

        # TODO: here we could implement permission check for 'shared-editing' playlists
        obj = Playlist.objects.get(pk=int(kwargs['pk']))
        if not obj.user == request.user:
            raise PermissionDenied

        return super(PlaylistEditView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        self.initial.update({
            'user': self.request.user,
            'd_tags': ','.join(t.name for t in self.object.tags)}
        )
        return self.initial

    def get_context_data(self, **kwargs):

        context = super(PlaylistEditView, self).get_context_data(**kwargs)

        context['action_form'] = ActionForm()
        context['user'] = self.request.user
        context['request'] = self.request

        if self.request.user.has_perm('importer.add_import') and not self.object.type == 'broadcast':
            context['can_upload_media'] = True
        else:
            context['can_upload_media'] = False

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # validation
        if form.is_valid():
            self.object.tags = form.cleaned_data['d_tags']

            # temporary instance to validate inline forms against
            tmp = form.save(commit=False)

            form.save()
            form.save_m2m()

            return HttpResponseRedirect('#')
        else:

            from base.utils.form_errors import merge_form_errors
            form_errors = merge_form_errors([form, ])

            return self.render_to_response(self.get_context_data(form=form, form_errors=form_errors))


@login_required
def playlist_convert(request, pk, type):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)

    playlist, status = playlist.convert_to(type)
    if status:
        messages.add_message(request, messages.INFO,
                             _('Successfully converted "%s" to "%s"' % (playlist.name, playlist.get_type_display())))
    else:
        messages.add_message(request, messages.ERROR,
                             _('There occured an error while converting "%s"' % (playlist.name)))

    return HttpResponseRedirect(playlist.get_edit_url())


@login_required
def playlist_request_mixdown(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)

    mixdown = playlist.request_mixdown()

    if not mixdown:
        messages.add_message(request, messages.WARNING,
                             _(u'Unable to requested Mixdown for "{}"'.format(playlist.name)))
        return HttpResponseRedirect(playlist.get_absolute_url())

    if not mixdown['status'] == 3:

        # delete current mixdown
        if playlist.mixdown_file:
            playlist.mixdown_file.delete(False)
            Playlist.objects.filter(pk=pk).update(mixdown_file=None)

    messages.add_message(request, messages.INFO,
                         _(u'Requested Mixdown for "{}" - ETA: {}'.format(playlist.name, mixdown['eta'])))

    return HttpResponseRedirect(playlist.get_absolute_url())
