from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import render
import io
import urllib
import base64

def charts(request):
    medicoes = SensorData.objects.all()  

    if not medicoes:
        return render(request, "charts.html", {"grafico_url": None})

    valores = [m.distance for m in medicoes]  # Lista com os valores das medições
    

    valores = np.array(valores)
    medias = []
    amplitudes = []


    for i in range(0, len(valores), 5):
        bloco = np.array(valores[i:i+5])

        if len(bloco) == 5:  # Só calcula se o bloco tiver 5 elementos
            media_bloco = np.mean(bloco)
            medias.append(round(media_bloco, 2))  # Armazena a média arredondada
            bloco.sort()
            amplitudes.append(bloco[-1]-bloco[0])

    
    # Cálculo das linhas de controle

    A2 = 0.577
    D3 = 0
    D4 = 2.114
    D2= 2.326
    amplitudes = np.array(amplitudes)
    clR = np.mean(amplitudes)
    medias = np.array(medias)
    clX = np.mean(medias)
    lsc = clX + clR*A2  # Limite Superior de Controle
    lic = clX - clR*A2  # Limite Inferior de Controle
    lscR = D4*clR
    licR = D3*clR
    outliersX = 0
    outliersR = 0

    for i in medias:
        if i >lsc or i <lic:
            outliersX +=1

    dp= clR/D2
    cpx = (lsc-lic)/(6*dp)
    print(cpx)
    cpkx1 = (lsc - clX)/(3*dp)
    cpkx2 = (clX -lic)/(3*dp)
    print(f"{cpkx1}")
    print(f"{cpkx2}")

    if cpkx1 <= cpkx2:
        cpkx =cpkx1
    else:
        cpkx = cpkx2

    print(f"{cpkx}")
    cpR = (lscR-licR)/(6*dp)
    cpkR1 = (lscR - clX)/(3*dp)
    cpkR2 = (clX -licR)/(3*dp)

    if cpkR1 <= cpkR2:
        cpkR =cpkR1
    else:
        cpkR = cpkR2

    for i in amplitudes:
        if i >lscR or i <licR:
            outliersR +=1


        #regra1X
    if outliersX == 0:
        regra1X = True
    else:
        regra1X = False

    #regra1R
    if outliersR == 0:
        regra1R = True
    else:
        regra1R = False


      #regra 2, 3, 4 do X
    sigma = np.std(medias, ddof=1)
    twoSigmaPos= clX + 2*sigma
    twoSigmaNeg= clX - 2*sigma

    oneSigmaPos= clX + sigma
    oneSigmaNeg= clX - sigma

    #regra 2 
    regra2X = True
    for i in range(0, len(medias)-2, 1):
        if medias[i] > twoSigmaPos:
            if medias[i+1] > twoSigmaPos or medias[i+2] > twoSigmaPos:
                regra2X = False
                break
        else:
            if medias[i+1] > twoSigmaPos and medias[i+2] > twoSigmaPos:
                regra2X = False
                break

        if medias[i] < twoSigmaNeg:
            if medias[i+1] < twoSigmaNeg or medias[i+2] < twoSigmaNeg:
                regra2X = False
                break
        else:
            if medias[i+1] < twoSigmaNeg and medias[i+2] < twoSigmaNeg:
                regra2X = False
                break

    #regra 3
    regra3X = True
    aux = 0
    for i in range(0, len(medias)-4, 1):
        j=i
        while j<=i+4:
            if medias[j] > oneSigmaPos:
                aux+=1
            j+=1

        if aux >= 4:
            regra3X = False
            break
        
        aux=0
        while j<=i+4:
            if medias[j] < oneSigmaNeg:
                aux+=1
            j+=1

        if aux >= 4:
            regra3X = False
            break

        aux=0

    #regra4 X
    regra4X = True
    aux2=0
    for i in range(0, len(medias)-8, 1):
        if medias[i] > clX:
            j=i
            while j<=i+8:
                if medias[j] > clX:
                    aux2+=1
                j+=1
            
            if aux2 ==9:
                regra4X = False
                break

            aux2=0
        else:
            j=i
            while j<=i+8:
                if medias[j] < clX:
                    aux2+=1
                j+=1
            if aux2 ==9:
                regra4X = False
                break
            aux2=0

    sigma = np.std(amplitudes, ddof=1)
    twoSigmaPosR= clR + 2*sigma
    twoSigmaNegR= clR - 2*sigma

    oneSigmaPosR= clR + sigma
    oneSigmaNegR= clR - sigma

    #regra 2 
    regra2R = True
    for i in range(0, len(amplitudes)-2, 1):
        if amplitudes[i] > twoSigmaPosR:
            if amplitudes[i+1] > twoSigmaPosR or amplitudes[i+2] > twoSigmaPosR:
                regra2R = False
                break
        else:
            if amplitudes[i+1] > twoSigmaPosR and amplitudes[i+2] > twoSigmaPosR:
                regra2R = False
                break

        if amplitudes[i] < twoSigmaNegR:
            if amplitudes[i+1] < twoSigmaNegR or amplitudes[i+2] < twoSigmaNegR:
                regra2R = False
                break
        else:
            if amplitudes[i+1] < twoSigmaNegR and amplitudes[i+2] < twoSigmaNegR:
                regra2R = False
                break

    #regra 3
    regra3R = True
    aux = 0
    for i in range(0, len(amplitudes)-4, 1):
        j=i
        while j<=i+4:
            if amplitudes[j] > oneSigmaPosR:
                aux+=1
            j+=1

        if aux >= 4:
            regra3R = False
            break
        
        aux=0
        while j<=i+4:
            if amplitudes[j] < oneSigmaNegR:
                aux+=1
            j+=1

        if aux >= 4:
            regra3R = False
            break

        aux=0

    #regra4 X
    regra4R = True
    aux2=0
    for i in range(0, len(amplitudes)-8, 1):
        if amplitudes[i] > clR:
            j=i
            while j<=i+8:
                if amplitudes[j] > clR:
                    aux2+=1
                j+=1
            
            if aux2 ==9:
                regra4R = False
                break

            aux2=0
        else:
            j=i
            while j<=i+8:
                if amplitudes[j] < clR:
                    aux2+=1
                j+=1
            if aux2 ==9:
                regra4R = False
                break
            aux2=0







        




    



    indices = np.arange(1, len(medias) + 1)  # Índices para o eixo X

    # Criando o gráfico
    plt.figure(figsize=(10, 4))
    plt.plot(indices, medias, marker='o', linestyle='-', color='#FF6501', label="Médias")
    plt.axhline(y=clX, color='gray', linestyle='dashdot', label="Linha Central")
    plt.axhline(y=lsc, color='#D3082A', linestyle='dashed', label="Limite Superior")
    plt.axhline(y=lic, color='#D3082A', linestyle='dashed', label="Limite Inferior")
    plt.xlabel("Amostras")
    plt.ylabel("Média")
    # ax = plt.gca()
    # ax.set_xticks(range(1, len(medias) + 1))
    plt.legend()
    plt.grid(True)

    # Converter gráfico para base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    grafico_base64 = base64.b64encode(buffer.getvalue()).decode()
    grafico_url = f"data:image/png;base64,{grafico_base64}"


    # Criando o gráfico
    plt.figure(figsize=(10, 4))
    plt.plot(indices, amplitudes, marker='o', linestyle='-', color='#FF6501', label="Médias")
    plt.axhline(y=clR, color='gray', linestyle='dashdot', label="Linha Central")
    plt.axhline(y=lscR, color='#D3082A', linestyle='dashed', label="Limite Superior")
    plt.axhline(y=licR, color='#D3082A', linestyle='dashed', label="Limite Inferior")
    plt.xlabel("Amostras")
    plt.ylabel("Média")
    # ax = plt.gca()
    # ax.set_xticks(range(1, len(medias) + 1))
    plt.legend()
    plt.grid(True)

    # Converter gráfico para base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    grafico_base64 = base64.b64encode(buffer.getvalue()).decode()
    grafico_urlR = f"data:image/png;base64,{grafico_base64}"

    print(regra4X)

    

    return render(request, 'charts.html', {'grafico_url': grafico_url,
                                           'grafico_urlR': grafico_urlR,
                                            'lsc': round(lsc,3), 
                                            'lic': round(lic,3) ,
                                            'lscR': round(lscR,3) , 
                                            'licR':round(licR,3) ,
                                            'cpx':round(cpx,3)  ,
                                            'cpkx':round(cpkx,3) ,
                                            'cpR':round(cpR,3) ,
                                            'cpkR':round(cpkR,3) ,
                                            'amostra': len(medias),
                                            'outliersX': outliersX,
                                            'outliersR': outliersR,
                                            'regra1X': regra1X,
                                            'regra2X': regra2X,
                                            'regra3X': regra3X,
                                            'regra4X': regra4X,
                                            'regra1R': regra1R,
                                            'regra2R': regra2R,
                                            'regra3R': regra3R,
                                            'regra4R': regra4R})




@csrf_exempt
def receive_sensor_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            distance = data.get("distance")

            if distance is not None:
                SensorData.objects.create(distance=distance)
                return JsonResponse({"message": "Data saved successfully"}, status=201)
            else:
                return JsonResponse({"error": "Invalid data"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
