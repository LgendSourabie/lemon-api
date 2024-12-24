from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from lemon_authentication.serializers import UserSerializer
from django.http import Http404
from lemon_authentication.permissions import IsManager, IsSingleManager
# Create your views here.


class ManagerView(generics.ListCreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]


    def get_serializer_context(self):
        return {"request":self.request}

    def list(self, request, *args, **kwargs):

        manager_users = User.objects.filter(groups__name = "Manager")
        serializer = UserSerializer(manager_users, many = True, context = {"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = request.data.get('id',None)
            if user:
                try:
                    manager_group = Group.objects.get(name = "Manager")
                    manager_group.user_set.add(user)
                    return Response({"message":"user successfully added to manager group."}, status=status.HTTP_201_CREATED)
                except Group.DoesNotExist:
                    return Response({"error": "Manager group does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"error": "Id field is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SingleManagerView(generics.RetrieveDestroyAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSingleManager]

    def get_serializer_context(self):
        return {"request":self.request}
    
    def get_model_or_404(self, model,parameter, flag='user'):
        try:
            if flag == 'user':
                model = model.objects.get(pk = parameter)
            elif flag == 'group':
                model = model.objects.get(name = parameter)
        except model.DoesNotExist:
            raise Http404({f"{model} not found"})
        return model

    def delete(self, request, pk):
        
        user = self.get_model_or_404(model=User,parameter=pk)
        manager_group = self.get_model_or_404(model=Group,parameter="Manager", flag='group')
        manager_group.user_set.remove(user)
        return Response({"message":"user successfully removed from the manager group."}, status=status.HTTP_200_OK)
    


class DeliveryCrewView(generics.ListCreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]


    def get_serializer_context(self):
        return {"request":self.request}

    def list(self, request, *args, **kwargs):

        delivery_crew_users = User.objects.filter(groups__name = "Delivery crew")
        serializer = UserSerializer(delivery_crew_users, many = True, context = {"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = request.data.get('id',None)
            if user:
                try:
                    delivery_crew_group = Group.objects.get(name = "Delivery crew")
                    delivery_crew_group.user_set.add(user)
                    return Response({"message":"user successfully added to delivery crew group."}, status=status.HTTP_201_CREATED)
                except Group.DoesNotExist:
                    return Response({"error": "Delivery crew group does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"error": "Id field is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SingleDeliveryCrewView(generics.RetrieveDestroyAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSingleManager]

    def get_serializer_context(self):
        return {"request":self.request}
    
    def get_model_or_404(self, model,parameter, flag='user'):
        try:
            if flag == 'user':
                model = model.objects.get(pk = parameter)
            elif flag == 'group':
                model = model.objects.get(name = parameter)
        except model.DoesNotExist:
            raise Http404({f"{model} not found"})
        return model

    def delete(self, request, pk):
        
        user = self.get_model_or_404(model=User,parameter=pk)
        delivery_crew_group = self.get_model_or_404(model=Group,parameter="Delivery crew", flag='group')
        delivery_crew_group.user_set.remove(user)
        return Response({"message":"user successfully removed from the delivery crew group."}, status=status.HTTP_200_OK)