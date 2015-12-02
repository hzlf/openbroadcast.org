#-*- coding: utf-8 -*-
import logging
import shutil

import sys
from django.conf import settings
from django.core.management.base import NoArgsCommand, LabelCommand, BaseCommand

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)

log = logging.getLogger(__name__)

class MediaFix(object):

    def __init__(self, * args, **kwargs):
        self.verbosity = int(kwargs.get('verbosity', 1))

    def copy_from_import(self):

        from alibrary.models import Media

        print
        print '-----------------------------------------------'
        print 'replacing corrupt files with import versions'
        print '-----------------------------------------------'
        print

        qs = Media.objects.filter(base_format='m4a', id__gte=387750)

        print 'files in qs:   %s' % qs.count()

        for m in qs:

            print '%s' % (m.name)

            src = m.importfile_media.all()[0].file.path
            dst = m.master.path

            print 'src: %s' % src
            print 'dst: %s' % dst

            shutil.copy(src, dst)

            print


    def reprocess_master_meta(self):

        from alibrary.models import Media

        print
        print '-----------------------------------------------'
        print 'replacing corrupt files with import versions'
        print '-----------------------------------------------'
        print

        qs = Media.objects.filter(master_duration__isnull=True).nocache()

        print 'files in qs:   %s' % qs.count()


        for m in qs[0:500000]:
            try:
                if not m.master:
                    print 'no master assigned for: %s' % m
                else:
                    m.process_master_info()
                    m.save()
            except IOError as e:
                print e





class Command(BaseCommand):

    def add_arguments(self, parser):

        # Positional arguments
        parser.add_argument('action')

        # Named (optional) arguments
        parser.add_argument('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete poll instead of closing it')

    def handle(self, *args, **options):

        action = options.get('action', None)


        if action == 'reprocess_master_meta':

            runner = MediaFix()
            runner.reprocess_master_meta()
