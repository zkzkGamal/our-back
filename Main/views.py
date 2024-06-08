from rest_framework import generics, response, status
from rest_framework.exceptions import PermissionDenied
from .models import Drugs_Order, Order_Items
from .serializers import OrderSerializer, OrderItemSerializer
from .permissions import IsAuthenticatedOrReadOnly  

class MyOrders(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            profile = user.profile
            return Drugs_Order.objects.filter(profile=profile)
        raise PermissionDenied("You must be authenticated to access this endpoint.")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ModifyMyOrder(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drugs_Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MyItems(generics.ListCreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            profile = user.profile
            orders = Drugs_Order.objects.filter(profile=profile)
            return Order_Items.objects.filter(drugs_order__in=orders)
        raise PermissionDenied("You must be authenticated to access this endpoint.")

class ModifyMyItems(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order_Items.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]











from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Blog_Posts, Comment_Posts
from .serializers import BlogPostSerializer, CommentPostSerializer

class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = Blog_Posts.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a post.")
        if not self.request.user.groups.group_name=='doctors':
            raise PermissionDenied("You must be a doctor to create a post.")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(doctor=self.request.user.doctor_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BlogPostRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog_Posts.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.user.groups.group_name=='doctors':
            if obj.doctor.user != self.request.user:
                raise PermissionDenied("You must be a doctor to edit your posts.")
        return obj

    def put(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to update a blog post.")
        if not self.request.user.groups.group_name=='doctors':
            raise PermissionDenied("You must be a doctor to edit your posts.")
        
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to delete a blog post.")
        if not self.request.user.groups.group_name=='doctors':
            raise PermissionDenied("You must be a doctor to delete a blog post.")
        
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentPostCreateView(generics.CreateAPIView):
    queryset = Comment_Posts.objects.all()
    serializer_class = CommentPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a comment.")
        serializer.save(profile=self.request.user.profile)

class CommentPostRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment_Posts.objects.all()
    serializer_class = CommentPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to update a comment.")
        if self.request.user.profile != self.get_object().profile:
            raise PermissionDenied("You can only update your own comments.")
        
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to delete a comment.")
        if request.user.profile != self.get_object().profile:
            raise PermissionDenied("You can only delete your own comments.")
        
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


