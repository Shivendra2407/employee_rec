from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response as RestResponse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .forms import EmployeeCreationForm
from locations.models import City
from .models import Gender, Employee
from rest_framework import generics
from .serializers import EmployeeListSerializer
from .paginations import SmallPagesPagination


class EmployeeView(APIView):
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        context = {}
        status = HTTP_200_OK
        try:
            context['form'] = EmployeeCreationForm()
            context['message'] = ''
            context['cities'] = City.objects.all()
            context['genders'] = Gender.objects.all()
        except Exception as e:
            print("Exception in HomeView GET API VIEW -> "+str(e))
            context = {}
        finally:
            return RestResponse(context, status=HTTP_200_OK, template_name='index.html')

    def post(self, request, *args, **kwargs):
        context = {}
        status = HTTP_200_OK
        try:
            form = EmployeeCreationForm(request.POST)
            if form.is_valid():
                new_employee_inst = form.save()
                context['message'] = 'Saved record with id '+str(new_employee_inst.id)
            else:
                context['message'] = 'Server side validation error : '+'  '.join(field+' : '+' , '.join(err for err in error_list) for field,error_list in form.errors.items())
                context['error'] = True
        except Exception as e:
            print("Exception occurred in HomeView GET API VIEW ->  "+str(e))
            status = HTTP_400_BAD_REQUEST
            context['message'] = 'Failure'
            context['error'] = True
        finally:
            context['form'] = EmployeeCreationForm()
            return RestResponse(context, status=status, template_name='index.html')


class EmployeeUpdatetView(APIView):
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        try:
            pan = request.data.get("pan_number")
            if pan:
                email = request.data.get("email")
                city_id = request.data.get("city")
                instance = Employee.objects.filter(pan_number=pan)
                if len(instance) == 1:
                    instance = instance[0]
                    instance.city_id = city_id
                    instance.email = email
                    instance.save()
                    return RestResponse({'data': 'Success'}, status=HTTP_200_OK)
                else:
                    return RestResponse({'data': 'Failure'}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception while updating employee data "+str(e))
            return RestResponse({'data': 'Failure'}, status=HTTP_400_BAD_REQUEST)


class DeleteEmployeAPIView(APIView):
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        try:
            instance = Employee.objects.filter(pan_number=request.data.get('pan_number'))
            if len(instance) == 1:
                instance.delete()
                return RestResponse({'data': 'Success'}, status=HTTP_200_OK)
            else:
                return RestResponse({'data':'Failure'},status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception while deleting employee data " + str(e))
            return RestResponse({'data': 'Failure'}, status=HTTP_400_BAD_REQUEST)


class GenericSearch(generics.ListAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = EmployeeListSerializer
    queryset = Employee.objects.all()

    def post(self, request):
        try:
            params = request.data
            queryset = Employee.objects.filter(**params)
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page,many=True)
            data = serializer.data

            return RestResponse({'data': 'Success','result':data}, status=HTTP_200_OK)
        except Exception as e:
            print("Exception in GenericSearch post -> "+str(e))
            return RestResponse({'data': 'Failure'}, status=HTTP_400_BAD_REQUEST)


class EmployeeListAPIView(generics.ListAPIView):
    renderer_classes = (JSONRenderer,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer
    pagination_class = SmallPagesPagination

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(kwargs)
        orderColumnIndex = request.POST.get('order[0][column]')
        columnName=request.POST.get('columns['+orderColumnIndex+'][data]')
        row = request.POST.get('start');
        rowperpage = request.POST.get('length');
        columnSortOrder = request.POST.get('order[0][dir]');
        searchValue = request.POST.get('search[value]');
        print(orderColumnIndex, columnName, row, rowperpage, columnSortOrder, searchValue)
        self.queryset_ordering(columnName, columnSortOrder)
        if searchValue.strip():
            self.queryset_searching(searchValue)
        obj = self.get(self, request, *args, **kwargs)
        return obj

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return RestResponse(serializer.data)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, self.request)

    def queryset_ordering(self, columnName, columnSortOrder):
        if columnName:
            if columnName == "name":
                if columnSortOrder == "asc":
                    name = "name"
                else:
                    name = "-name"
            elif columnName == "pan_number":
                if columnSortOrder == "asc":
                    name = "pan_number"
                else:
                    name = "-pan_number"
            elif columnName == "city":
                if columnSortOrder == "asc":
                    name = "city__name"
                else:
                    name = "-city__name"
            self.queryset = self.queryset.order_by(name)

    def queryset_searching(self, searchValue):
        if searchValue:
            self.queryset = self.queryset.filter(name__icontains=searchValue) |\
                            self.queryset.filter(city__name__icontains=searchValue) |\
                            self.queryset.filter(email__icontains=searchValue) |\
                            self.queryset.filter(age__icontains=searchValue)|\
                            self.queryset.filter(pan_number__icontains=searchValue)





