from django.contrib import admin
from .models import Mpolynom
from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.contrib import admin
from django import forms
from django.contrib.admin import helpers
from django.contrib.admin.options import csrf_protect_m, IS_POPUP_VAR
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text

# for nonfield errors to show correctly
from django.forms.forms import NON_FIELD_ERRORS





class MpolynomAdminForm(forms.ModelForm):
    class Meta:
            model = Mpolynom
            fields = ('mpolynomyal', 'structure_name', 'keywords', 'comments', 'references','links')
    def clean(self):
        input_string = self.cleaned_data.get('mpolynomyal')
        s = []
        balanced = True
        index = 0
        while index < len(input_string) and balanced:
            token = input_string[index]
            if token == "(":
                s.append(token)
            elif token == ")":
                if len(s) == 0:
                    balanced = False
                else:
                    s.pop()
            index += 1
        val = balanced and len(s) == 0
        if not val:
            raise ValidationError('Parentheses do not match. Please correct the M-polynomial.')
        return self.cleaned_data

class TestModelAdmin(admin.ModelAdmin):
    form = MpolynomAdminForm

    # def save_model(self, request, obj, form, change):

    #     raise Exception('test exception')

    def save_model(self, request, obj, form, change):
        obj.author = request.user.username
        obj.save()

    # makes database and parentheses errors displayed on the admin page when adding M-polynomial
    def add_view(self, request, form_url='', extra_context=None):
        try:
            return super(TestModelAdmin, self).add_view(request, form_url, extra_context)
        except (IntegrityError, DatabaseError) as e:
            # request.method = 'GET'
            # messages.error(request, e)
            # return super(TestModelAdmin, self).add_view(request, form_url, extra_context)
            if str(e) == 'UNIQUE constraint failed: search_mpolynom.structure_name':
                e = 'Structure name already exists! Check if the M-polynomial already exists in the database.'
            model = self.model
            opts = model._meta

        # ModelForm = MpolynomAdminForm
            formsets = []
            inline_instances = self.get_inline_instances(request, None)
            form = MpolynomAdminForm(request.POST, request.FILES)
            form.is_valid()
            
            # make faked nonfield error
            # see http://stackoverflow.com/questions/8598247/how-to-append-error-message-to-form-non-field-errors-in-django
            form._errors[NON_FIELD_ERRORS] = form.error_class([e])

            # We may handle exception here (just to save indentation)
            adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)),
                self.get_prepopulated_fields(request),
                self.get_readonly_fields(request),
                model_admin=self)
            media = self.media + adminForm.media

            inline_admin_formsets = []
            for inline, formset in zip(inline_instances, formsets):
                fieldsets = list(inline.get_fieldsets(request))
                readonly = list(inline.get_readonly_fields(request))
                prepopulated = dict(inline.get_prepopulated_fields(request))
                inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                    fieldsets, prepopulated, readonly, model_admin=self)
                inline_admin_formsets.append(inline_admin_formset)
                media = media + inline_admin_formset.media
            context = {
                'title': _('Add %s') % force_text(opts.verbose_name),
                'adminform': adminForm,
                'is_popup': IS_POPUP_VAR in request,
                'media': media,
                'inline_admin_formsets': inline_admin_formsets,
                'errors': helpers.AdminErrorList(form, formsets),
                'app_label': opts.app_label,
                'preserved_filters': self.get_preserved_filters(request),
            }
            context.update(extra_context or {})
            return self.render_change_form(request, context, form_url=form_url, add=True)

    # makes database and parentheses errors displayed on the admin page when changing M-polynomial
    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            return super(TestModelAdmin, self).change_view(request, object_id, form_url, extra_context)
        except (IntegrityError, DatabaseError) as e:
            if str(e) == 'UNIQUE constraint failed: search_mpolynom.structure_name':
                e = 'Structure name already exists! Check if the M-polynomial already exists in the database.'
            model = self.model
            opts = model._meta

        # ModelForm = MpolynomAdminForm
            formsets = []
            inline_instances = self.get_inline_instances(request, None)
            form = MpolynomAdminForm(request.POST, request.FILES)
            form.is_valid()
            
            # make faked nonfield error
            # see http://stackoverflow.com/questions/8598247/how-to-append-error-message-to-form-non-field-errors-in-django
            form._errors[NON_FIELD_ERRORS] = form.error_class([e])

            # We may handle exception here (just to save indentation)
            adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)),
                self.get_prepopulated_fields(request),
                self.get_readonly_fields(request),
                model_admin=self)
            media = self.media + adminForm.media

            inline_admin_formsets = []
            for inline, formset in zip(inline_instances, formsets):
                fieldsets = list(inline.get_fieldsets(request))
                readonly = list(inline.get_readonly_fields(request))
                prepopulated = dict(inline.get_prepopulated_fields(request))
                inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                    fieldsets, prepopulated, readonly, model_admin=self)
                inline_admin_formsets.append(inline_admin_formset)
                media = media + inline_admin_formset.media
            context = {
                'title': _('Add %s') % force_text(opts.verbose_name),
                'adminform': adminForm,
                'is_popup': IS_POPUP_VAR in request,
                'media': media,
                'inline_admin_formsets': inline_admin_formsets,
                'errors': helpers.AdminErrorList(form, formsets),
                'app_label': opts.app_label,
                'preserved_filters': self.get_preserved_filters(request),
            }
            context.update(extra_context or {})
            return self.render_change_form(request, context, form_url=form_url, add=True)
           
 

    #non-superuser users can see only their inputs
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            # by_author = qs.filter(author=request.user)
            # by_author_waiting = by_author.filter(status="waiting")
            # nb_author_waiting = by_author_waiting.count()
            # if nb_author_waiting > 10:

            return qs.filter(author=request.user)

    # if user has more than 100 unresolved(status waiting) objects cant add new
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            by_author = Mpolynom.objects.filter(author=request.user)
            by_author_waiting = by_author.filter(status="waiting")
            nb_author_waiting = by_author_waiting.count()
            if nb_author_waiting > 100:
                return False
            else:
                return True


    def changeform_view(self, request, *args, **kwargs):
        try:
            return super().changeform_view(request, *args, **kwargs)
        except IOError as err:
            self.message_user(request, str(err), level=messages.ERROR)
            return HttpResponseRedirect(request.path)


    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            if obj and obj.status == 'approved':
                return self.readonly_fields + ('mpolynomyal', 'structure_name', 'Mid', 'author','published_recently', 'status', 'keywords', 'comments', 'references', 'links')
            return self.readonly_fields + ('status',)
        return self.readonly_fields

    #kaj s tem
    # # # # def changelist_view(self, request, extra_context=None):    
    # # # #     if not request.user.is_superuser:
    # # # #         self.list_display = ('mpolynomyal', 'structure_name', 'Mid', 'author','published_recently')
    # # # #     else:
    # # # #         self.list_display = ('mpolynomyal', 'structure_name', 'Mid', 'author','published_recently', 'status')
    # # # #     return super(TestModelAdmin, self).changelist_view(request, extra_context)
    list_display = ('mpolynomyal', 'structure_name', 'Mid', 'author','published_recently', 'status')
    list_filter = ['publication_date']
    search_fields = ['mpolynomyal', 'structure_name','author','Mid']
admin.site.register(Mpolynom, TestModelAdmin)



