from tastypie.serializers import Serializer
import urlparse

class urlencodeSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
        }
    def from_urlencode(self, data,options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v)>1 else v[0] )
            for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self,content):
        pass

class MultiPartResource(object):
    def deserialize(self, request, data, format=None):
        try:
            # print request
            if not format:
               format = request.Meta.get('CONTENT_TYPE', 'application/json')
            if format == 'application/x-www-form-urlencoded':
               return request.POST
            if format.startswith('multipart/form-data'):
               data = request.POST.copy()
               data.update(request.FILES)
               return data
        except Exception as e:
            print e
        return super(MultiPartResource, self).deserialize(request, data, format)
