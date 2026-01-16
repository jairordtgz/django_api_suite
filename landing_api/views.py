from django.shortcuts import render

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Firebase Admin SDK
from firebase_admin import db

# Python
from datetime import datetime


class LandingAPI(APIView):
    # Atributos solicitados
    name = "Landing API"
    collection_name = "votes"  # nombre del nodo/colección en Realtime Database

    def get(self, request):

      # Referencia a la colección
      ref = db.reference(f'{self.collection_name}')

      # get: Obtiene todos los elementos de la col ección
      data = ref.get()

      # Devuelve un arreglo JSON
      return Response(data, status=status.HTTP_200_OK)

    def post(self, request):

      data = request.data

      # Referencia a la colección
      ref = db.reference(f'{self.collection_name}')

      current_time  = datetime.now()
      custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
      data.update({"timestamp": custom_format })

      # push: Guarda el objeto en la colección
      new_resource = ref.push(data)

      # Devuelve el id del objeto guardado
      return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)

