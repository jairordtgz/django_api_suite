from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
    # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)

    
    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
      """Vista para operar sobre un único elemento identificado por su `id`.

      Métodos soportados:
      - PUT: reemplazo completo del elemento (requiere `id` en el cuerpo y debe coincidir con la URL).
      - PATCH: actualización parcial de campos.
      - DELETE: eliminación lógica (setear `is_active` a False).
      """

      def get_item(self, item_id):
        for idx, item in enumerate(data_list):
          if item.get('id') == str(item_id):
            return idx, item
        return None, None

      def put(self, request, item_id):
        data = request.data

        if 'id' not in data:
          return Response({'error': 'El campo "id" es obligatorio en el cuerpo.'}, status=status.HTTP_400_BAD_REQUEST)

        if str(data.get('id')) != str(item_id):
          return Response({'error': 'El id del cuerpo no coincide con el id de la URL.'}, status=status.HTTP_400_BAD_REQUEST)

        idx, item = self.get_item(item_id)
        if item is None:
          return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Validación mínima: solicitar name y email para el reemplazo completo
        if 'name' not in data or 'email' not in data:
          return Response({'error': 'Faltan campos requeridos para PUT: name y email.'}, status=status.HTTP_400_BAD_REQUEST)

        # Reemplaza completamente el elemento excepto el id
        new_item = {
          'id': str(item_id),
          'name': data.get('name'),
          'email': data.get('email'),
          'is_active': data.get('is_active', True)
        }

        data_list[idx] = new_item
        return Response({'message': 'Elemento reemplazado correctamente.', 'data': new_item}, status=status.HTTP_200_OK)

      def patch(self, request, item_id):
        data = request.data
        idx, item = self.get_item(item_id)
        if item is None:
          return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Actualiza solo los campos presentes en el cuerpo
        updated = item.copy()
        for key in ('name', 'email', 'is_active'):
          if key in data:
            updated[key] = data[key]

        data_list[idx] = updated
        return Response({'message': 'Elemento actualizado parcialmente.', 'data': updated}, status=status.HTTP_200_OK)

      def delete(self, request, item_id):
        idx, item = self.get_item(item_id)
        if item is None:
          return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not item.get('is_active', True):
          return Response({'message': 'Elemento ya está eliminado.'}, status=status.HTTP_200_OK)

        data_list[idx]['is_active'] = False
        return Response({'message': 'Elemento eliminado lógicamente.'}, status=status.HTTP_200_OK)