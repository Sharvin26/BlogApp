from .blog import BlogsApi, BlogApi
from .user import SignUpApi, RefreshAccessTokenApi, LoginApi, GetUserDetailsApi
from .confirm_email import SendConfirmEmail, ConfirmEmail
from .reset_password import ForgetPassword, ResetPassword

def initialize_urls(api):
    api.add_resource(BlogsApi, "/api/blogs")
    api.add_resource(BlogApi, "/api/blog/<id>")
    api.add_resource(GetUserDetailsApi, "/api/user", "/api/user/<username>")
    api.add_resource(SignUpApi, "/api/user/register")
    api.add_resource(RefreshAccessTokenApi, "/api/user/refresh")
    api.add_resource(LoginApi, "/api/user/login")
    api.add_resource(SendConfirmEmail, "/api/user/send/confirm")
    api.add_resource(ConfirmEmail, "/api/user/confirm")
    api.add_resource(ForgetPassword, "/api/user/forget")
    api.add_resource(ResetPassword, "/api/user/reset")