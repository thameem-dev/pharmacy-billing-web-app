# # from django.shortcuts import redirect

# # class RoleMiddleware:
# #     def __init__(self, get_response):
# #         self.get_response = get_response

# #     def __call__(self, request):

# #         if not request.user.is_authenticated:
# #             return self.get_response(request)

# #         role = request.user.role  # assuming role stored in user model

# #         # Restriction rules for all apps
# #         rules = {
# #             "system_admin": ["/adduser/","/loginhistory","/dashboard/"],   # admin full access
# #             "biller": [
# #                "/stock/stockslist","/dashboard/","/bill/billentry","/dashboard/"

# #             ],
# #             "inventory": [
# #                 "/stock/addstock/","/stock/addmedicine/","/stock/stockslist","/dashboard/",
# #             ],
# #             "manager": [
# #                 "/stock/addstock/","/stock/addmedicine/","/stock/stockslist","/dashboard/",
# #             ],
# #         }

# #         blocked_urls = rules.get(role, [])

# #         for url in blocked_urls:
# #             if request.path.startswith(url):
# #                 return redirect("dashboard")

# #         return self.get_response(request)
# from django.shortcuts import redirect

# class RoleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):

#         if not request.user.is_authenticated:
#             return self.get_response(request)

#         role = getattr(request.user, "role", None)

#         # Allowed URLs for each role
#         allowed_urls = {
#             "system_admin": ["/adduser/", "/loginhistory/", "/dashboard/,","/logout/"],
#             "biller": ["/stock/stockslist/", "/bill/billentry/", "/dashboard/","/logout/"],
#             "inventory": ["/stock/addstock/", "/stock/addmedicine/", "/stock/stockslist/", "/dashboard/","/logout/"],
#             "manager": ["/stock/addstock/", "/stock/addmedicine/", "/stock/stockslist/", "/dashboard/","/logout/"],
#         }

#         # Get allowed urls for current role
#         role_allowed = allowed_urls.get(role, [])

#         # If current path is NOT allowed, redirect
#         path = request.path
#         if path not in role_allowed:
#             return redirect("/dashboard/")   # or use URL name with reverse
                

#         return self.get_response(request)
from django.shortcuts import redirect

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path

        # Always allow login, logout, static files
        public_urls = ["/login/", "/logout/", "/static/", "/media/",'/admin/']
        for p in public_urls:
            if path.startswith(p):
                return self.get_response(request)

        # If user not logged in → must login
        if not request.user.is_authenticated:
            return redirect("/login/")

        role = getattr(request.user, "role", None)

        allowed_urls = {
            "system_admin": [
                "/adduser/", "/loginhistory/", "/dashboard/", "/logout/"
            ],
            "biller": [
                "/stock/stockslist/", "/bill/billentry/", "/dashboard/", "/logout/"
            ],
            "inventory": [
                "/stock/addstock/", "/stock/addmedicine/", "/stock/stockslist/",
                "/dashboard/", "/logout/"
            ],
            "manager": [
                "/stock/addstock/", '/bill/salesreport/', "/stock/addmedicine/", "/stock/stockslist/",
                "/dashboard/", "/logout/"
            ],
        }

        role_allowed = allowed_urls.get(role, [])

        # Check allowed paths
        for allowed in role_allowed:
            if path.startswith(allowed):
                return self.get_response(request)

        # Not allowed → redirect
        return redirect("/dashboard/")
