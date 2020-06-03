from .blog import BlogsApi, BlogApi

def initialize_urls(api):
    api.add_resource(BlogsApi, "/api/blogs")
    api.add_resource(BlogApi, "/api/blog/<id>")