from django.contrib.sitemaps import Sitemap
from predict.models import Game
from users.models import Profile
from django.urls import reverse



class GameSitemap(Sitemap):

    changefreq = "daily"  # Change frequency, you can adjust this based on your needs.
    priority = 0.8  # Priority of this particular content, again adjust as you see fit.
    limit = 100  # Set the limit to 100 entries per sitemap page

    def items(self):
            return Game.objects.all().order_by('-date_posted')

    def lastmod(self, obj):
        # Returns the timestamp when the post was last modified.
        return obj.date_posted
    

    def location(self, obj):
        # Assuming you have a detail view named 'post_detail' that takes a post's id as argument.
        # Adjust the reverse URL pattern if your setup is different.
        return reverse('edit-predict', args=[obj.id])
    




from django.http import HttpResponse,Http404

from django.http import HttpResponse

def sitemap_index(request):
    sitemap_urls = []
  
    for sitemap_name, sitemap_class in sitemaps.items():
        sitemap = sitemap_class()
        total_items = sitemap.items().count()
        num_pages = (total_items // sitemap.limit) + (1 if total_items % sitemap.limit else 0)
        for p in range(1, num_pages + 1):
            sitemap_urls.append(request.build_absolute_uri(f'/sitemap-{sitemap_name.lower()}.xml?p={p}'))

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sitemap_urls:
        xml_content += f'   <sitemap>\n      <loc>{url}</loc>\n   </sitemap>\n'
    xml_content += '</sitemapindex>'

    return HttpResponse(xml_content, content_type='application/xml')



from django.http import HttpResponse
from django.utils.http import http_date
from .sitemaps import GameSitemap  # Import your GameSitemap class
from django.core.paginator import Paginator

def custom_sitemap_view(request, sitemap_name):
    sitemap_class = sitemaps.get(sitemap_name)
    if not sitemap_class:
        raise Http404("No sitemap found for the given name.")

    sitemap = sitemap_class()
    page_number = request.GET.get('p', 1)
    paginator = Paginator(sitemap.items(), sitemap.limit)
    page = paginator.get_page(page_number)

    # Generate XML content
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for item in page:
        loc = request.build_absolute_uri(sitemap.location(item))
        lastmod = sitemap.lastmod(item).strftime("%Y-%m-%d") if sitemap.lastmod(item) else ""
        xml_content += f'   <url>\n      <loc>{loc}</loc>\n'
        if lastmod:
            xml_content += f'      <lastmod>{lastmod}</lastmod>\n'
        xml_content += '   </url>\n'

    xml_content += '</urlset>'

    response = HttpResponse(xml_content, content_type='application/xml')
    return response

