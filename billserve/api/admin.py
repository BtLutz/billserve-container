from django.contrib import admin

from billserve.api.models import *

admin.site.register(Bill)
admin.site.register(Legislator)
admin.site.register(Action)
admin.site.register(Sponsorship)
admin.site.register(Cosponsorship)
admin.site.register(Representative)
admin.site.register(Senator)
admin.site.register(State)
admin.site.register(District)
admin.site.register(Party)
admin.site.register(BillSummary)
admin.site.register(Committee)
admin.site.register(LegislativeSubject)
