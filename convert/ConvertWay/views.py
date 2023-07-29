# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from .panelCode import ats,bd,dlv,dtdc,ekart,smartr,xb,ecom
import os

def index(request):
    # return HttpResponse("this is the home page")
    if(request.method == "POST"):
        courier = request.POST.get('courier')
        name = request.FILES.get('fileIn')
        # name = request.POST.get('')
        if(name is not None and courier == 'ATS'):
            response = ats(name,courier)
        if(name is not None and courier == 'BD'):
            response = bd(name, courier)
        if (name is not None and courier == 'DLV'):
            response = dlv(name, courier)
        if (name is not None and courier == 'DTDC'):
            response = dtdc(name, courier)
        if (name is not None and courier == 'EKART'):
            response = ekart(name, courier)
        if (name is not None and courier == 'SMARTR'):
            response = smartr(name, courier)
        if (name is not None and courier == 'XB'):
            response = xb(name, courier)
        if (name is not None and courier == 'ECOM'):
            response = ecom(name, courier)
        # params = {'check' : check}
        # return render(request,'panel.html',params)
        # response = FileResponse(open('/home/shipway/Django/combine/output.xlsx', 'rb'), as_attachment=True)
        if(response == "error"):
            return render(request,'panel.html' , {'check':False})
        return response

    return render(request,'panel.html')


