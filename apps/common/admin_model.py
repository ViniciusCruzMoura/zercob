from functools import reduce
from operator import or_
from django.db.models import Q
import io
import zipfile
from django.contrib import messages
from django.utils.html import format_html
from apps.common.bg import BackgroundTasks
from decimal import Decimal
from django import forms

class PhoneWidget(forms.TextInput):
    class Media:
        js = ("admin/js/phone_mask.js",)

    def __init__(self, attrs=None):
        attrs = attrs.copy() if attrs else {}

        attrs.setdefault("autocomplete", "tel")
        attrs.setdefault("inputmode", "tel")
        attrs.setdefault("placeholder", "+55 xx 9xxxx-xxxx")

        current_class = attrs.get("class", "")
        if "phone-mask" not in current_class.split():
            attrs["class"] = f"{current_class} phone-mask".strip()

        super().__init__(attrs=attrs)

class PercentageWidget(forms.TextInput):
    class Media:
        js = ("admin/js/percentage_mask.js",)

    def __init__(self, attrs=None):
        attrs = attrs.copy() if attrs else {}

        attrs.setdefault("autocomplete", "off")
        attrs.setdefault("inputmode", "decimal")
        attrs.setdefault("class", "")
        attrs.setdefault("placeholder", "%")

        if "percentage-mask" not in attrs["class"].split():
            attrs["class"] = (attrs["class"] + " percentage-mask").strip()

        super().__init__(attrs=attrs)

class BrazilianCpfCnpjWidget(forms.TextInput):
    class Media:
        js = ("admin/js/cpf_cnpj_mask.js",)

    def __init__(self, attrs=None):
        attrs = attrs or {}
        if attrs:
            attrs.update({"autocomplete": "off"})
        attrs.setdefault("class", "")
        attrs.setdefault("placeholder", "xxx.xxx.xxx-xx ou xx.xxx.xxx/xxxx-xx")
        if "cpf-cnpj-mask" not in attrs["class"].split():
            attrs["class"] = (attrs["class"] + " cpf-cnpj-mask").strip()
        super().__init__(attrs=attrs)

class BrazilianCurrencyWidget(forms.TextInput):
    class Media:
        js = ('admin/js/currency_formatter.js',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#         self.attrs['class'] = 'brazilian-currency'
#         self.attrs['placeholder'] = 'R$ 0,00'
        existing_classes = self.attrs.get("class", "")
        self.attrs["class"] = f"{existing_classes} brazilian-currency".strip()
        self.attrs.setdefault("placeholder", "R$ 0,00")

    def format_value(self, value):
        if value is None or value == '':
            return ''
        amount = Decimal(value) / 100
        return amount.quantize(Decimal('0.01')).to_eng_string().replace('.', ',')
    
def admin_model_get_form_widget(form, self, request, obj=None, **kwargs):
    # admin_model_get_form_currency_fields(self, request, obj=None, **kwargs)
    # admin_model_get_form_date_fields(self, request, obj=None, **kwargs)
    if getattr(self, "currency_fields", None) and self.currency_fields:
        for field_name in self.currency_fields:
            if field_name in form.base_fields:
                form.base_fields[field_name].widget = BrazilianCurrencyWidget(
                    attrs=form.base_fields[field_name].widget.attrs
                )
    if getattr(self, "cpf_cnpj_fields", None) and self.cpf_cnpj_fields:
        for field_name in self.cpf_cnpj_fields:
            if field_name in form.base_fields:
                form.base_fields[field_name].widget = BrazilianCpfCnpjWidget(
                    attrs=form.base_fields[field_name].widget.attrs
                )
    if getattr(self, "percentage_fields", None) and self.percentage_fields:
        for field_name in self.percentage_fields:
            if field_name in form.base_fields:
                form.base_fields[field_name].widget = PercentageWidget(
                    attrs=form.base_fields[field_name].widget.attrs
                )
    if getattr(self, "phone_fields", None) and self.phone_fields:
        for field_name in self.phone_fields:
            if field_name in form.base_fields:
                form.base_fields[field_name].widget = PhoneWidget(
                    attrs=form.base_fields[field_name].widget.attrs
                )

class ActionValidationTable():
    def __init__(self):
        self.result_error = []
        self.html_errors = ""
    def send(self, err, fil):
        self.result_error.append({"error": err, "file": fil})
    def html(self):
        self.html_errors = ""
        for err in self.result_error[:1000]:
            self.html_errors += f"""
            <tr>
              <td>{err.get("error")}</td>
              <td>{err.get("file")}</td>
            </tr>
            """
        _l = len(self.result_error)
        height = 70 + (_l * 30) if _l <= 8 else 300
        erro_msg = f"""
                <div class="card-body table-responsive p-0" style="height: {height}px;">
                    <table class="table table-sm">
                      <thead>
                        <tr>
                          <th style="color: #FFFFFF;">Erro</th>
                          <th style="color: #FFFFFF;">Arquivo</th>
                        </tr>
                      </thead>
                      <tbody>
                      {self.html_errors}
                      </tbody>
                    </table>
                </div>
                """
        return erro_msg
    def html_format(self):
        return format_html(self.html())
    def message(self, admin_model, request):
        if self.result_error:
            admin_model.message_user(request, self.html_format(), messages.ERROR)

def admin_model_get_search_results(self, request, queryset, search_term):
    queryset, use_distinct = super(type(self), self).get_search_results(request, queryset, search_term)
#     if search_term:
#         search_words = [word.strip() for word in search_term.split(',') if word.strip()]
#         if search_words:
#             q_objects = [Q(**{field + '__icontains': word.strip()})
#                                 for field in self.search_fields
#                                 for word in search_words]
#             q = request.GET.copy()
#             for field in list(q.dict().keys()):
#                 field = field.split('__')[0]
#                 if field not in set(vars(self.model).keys()):
#                     del q[field]
#             queryset |= self.model.objects.filter(reduce(or_, q_objects), **q.dict())
    # TODO 202607201056 na baseprodutiva eu uso outra implementação
    # para resolver algum bug que não lembro, acho q é por conta
    # dos filtros em ForeignKey, vou deixa isso aqui, vai q eu lembro
    # o pq das coisas......
    # TODO 202607281123 atualização... eu lembrei o pq... um usuario
    # que não tem permissão consegue ver um registro quando pesquisa,
    # esse era o bug, o get_queryset estava sendo ignorado
    if search_term:
        search_words = [word.strip() for word in search_term.split(',') if word.strip()]
        if search_words:
            q_objects = [Q(**{field + '__icontains': word.strip()})
                                for field in self.search_fields
                                for word in search_words]
            q = request.GET.copy()
            for field in list(q.dict().keys()):
                field = field.split('__')[0]
                if field not in set(vars(self.model).keys()):
                    del q[field]
            queryset = self.get_queryset(request).filter(reduce(or_, q_objects), **q.dict())
    else:
        q = request.GET.copy()
        if q:
            for field in list(q.dict().keys()):
                field = field.split('__')[0]
                if field not in set(vars(self.model).keys()):
                    del q[field]
            if q:
                queryset = queryset.filter(**q.dict())
    return queryset, use_distinct

def admin_model_download_files_as_zip(itens_selecionados, _fields):
    if not itens_selecionados or not _fields:
        return None
    if not isinstance(itens_selecionados, object) or not isinstance(_fields, list):
        return None

    bg = BackgroundTasks(wait_time=6, max_threads=4)
    itens = []

    def thread_download(items_ptr, item, _fields):
        for field in _fields:
            atributes = field.split("__")
            arquivos = item
            for index, _ in enumerate(atributes):
                if index == 0:
                    arquivos = getattr(item, atributes[0])
                else:
                    arquivos = getattr(arquivos, atributes[index])
            for arquivo in arquivos.all():
                file_name = arquivo.get_file_name()
                print("admin_model_download_files_as_zip::thread_download", file_name)
                if not file_name:
                    continue
                file_content = arquivo.get_link_content()
                if file_content:
                    items_ptr.append((file_name, file_content))

    for item in itens_selecionados:
        bg.create(thread_download, (itens, item, _fields))

    bg.start()
    bg.wait()

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for i in itens:
            zipf.writestr(i[0], i[1])

    zipf.close()
    zip_buffer.seek(0)


    return zip_buffer

def admin_model_download_files_as_zip_nothreads(itens_selecionados, _fields):
    if not itens_selecionados or not _fields:
        return None
    if not isinstance(itens_selecionados, object) or not isinstance(_fields, list):
        return None
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for obj in itens_selecionados:
            for field in _fields:
                atributes = field.split("__")
                arquivos = obj
                for index, _ in enumerate(atributes):
                    if index == 0:
                        arquivos = getattr(obj, atributes[0])
                    else:
                        arquivos = getattr(arquivos, atributes[index])
                for arquivo in arquivos.all():
                    file_name = arquivo.get_file_name()
                    if not file_name:
                        continue
                    file_content = arquivo.get_link_content()
                    if file_content:
                        zipf.writestr(file_name, file_content)
    zip_buffer.seek(0)
    return zip_buffer

def admin_model_save(self, ordered_methods=None, excluded_methods=None, *args, **kwargs):
    ordered_methods = ordered_methods or []
    excluded_methods = set(excluded_methods or [])
    try:
        for method_name in ordered_methods:
            if method_name in excluded_methods:
                continue
            method = getattr(self, method_name, None)
            if callable(method):
                method()
        for method_name in dir(self):
            if (
                method_name.startswith("update_")
                and method_name not in ordered_methods
                and method_name not in excluded_methods
            ):
                method = getattr(self, method_name)
                if callable(method):
                    method()
    except Exception as err:
        import traceback
        traceback.print_exc()
        print("FATAL ERROR admin_model_save:", err)
