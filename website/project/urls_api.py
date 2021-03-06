from abcast.api import BaseResource as AbcastBaseResource
from abcast.api import ChannelResource, EmissionResource
from alibrary.api import (
    MediaResource,
    SimpleMediaResource,
    ReleaseResource,
    SimpleReleaseResource,
    ArtistResource,
    LabelResource,
    SimplePlaylistResource,
    PlaylistResource,
    PlaylistItemPlaylistResource,
)
from api_base.api import BaseResource
from arating.api import VoteResource
from atracker.api import EventResource
from exporter.api import ExportResource, ExportItemResource
from importer.api import ImportResource, ImportFileResource
from profiles.api import UserResource
from tastypie.api import Api

api = Api()


try:

    # base
    api.register(BaseResource())

    # library
    api.register(MediaResource())
    api.register(SimpleMediaResource())
    api.register(ReleaseResource())
    api.register(SimpleReleaseResource())
    api.register(ArtistResource())
    api.register(LabelResource())
    api.register(SimplePlaylistResource())
    api.register(PlaylistResource())
    api.register(PlaylistItemPlaylistResource())

    # importer
    api.register(ImportResource())
    api.register(ImportFileResource())

    # exporter
    api.register(ExportResource())
    api.register(ExportItemResource())

    # abcast
    api.register(AbcastBaseResource())
    api.register(ChannelResource())

    # scheduler (legacy)
    api.register(EmissionResource())

    # profiles
    # api.register(ProfileResource())
    api.register(UserResource())

    # rating
    api.register(VoteResource())

    # atracker
    api.register(EventResource())

except Exception as e:
    print("unable to register API (v1) resources: {}".format(e))
