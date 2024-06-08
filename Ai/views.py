from django.shortcuts import render
from django.shortcuts import render
from rest_framework import generics , mixins , serializers , response , status
from . import models
from Main.permissions import IsAuthenticatedOrReadOnly
import pickle
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences
import os
# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from rest_framework.exceptions import PermissionDenied
# Create your views here.
def load_model():
    with open('Ai/toxic_model.json', 'r') as json_file:
        loaded_model_json = json_file.read()

    # Load the model architecture
    loaded_model = model_from_json(loaded_model_json)

    # Load the model weights
    loaded_model.load_weights("Ai/toxic_model_weights.h5")

    return loaded_model
class commen_serializer(serializers.Serializer):
    comment = serializers.CharField()
class check_comment(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = commen_serializer
    def post(self , request , *args , **kwargs):
        with open('Ai/tokenizer.pkl', 'rb') as handle:
            tokenizer_1 = pickle.load(handle)
        model = load_model()
        example_comment = self.request.POST.get('comment')
        example_tokenized = tokenizer_1.texts_to_sequences([example_comment])
        example_padded = pad_sequences(example_tokenized, maxlen=100)
        prediction = model.predict(example_padded)
        print("Toxicity prediction:", prediction)
        if prediction >=0.5:
            return response.Response(data={'message':'this comment is toxic', 'status':1})
        return response.Response(data={'message':'this comment is not toxic', 'status':0})

class message_ai_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.AI_Messages
        fields = '__all__'
class my_ai_messages(generics.GenericAPIView, mixins.ListModelMixin,mixins.DestroyModelMixin):
    def get_queryset(self):
        user = self.request.user
        if 'sessions' in self.kwargs:
            if user.is_authenticated:
                msg = models.AI_Messages.objects.filter(profile = user.profile.id , session_id = self.kwargs['sessions'])
                if msg.exists():
                    return msg
                return PermissionDenied('You must be the owner of the message to access this endpoint')
            raise PermissionDenied('You must be authendicated')
        if user.is_authenticated:
            msg = models.AI_Messages.objects.filter(profile=user.profile.id)
            if msg.exists():
                return msg
            return models.AI_Messages.objects.none()

        return models.AI_Messages.objects.none()            
    
    serializer_class = message_ai_serializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self , request , *args , **kwargs):
        return self.list(request , *args , **kwargs)
    def delete(self , request , *args , **kwargs):
        return self.destroy(request , *args , **kwargs)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sessions(request):
    user = request.user
    if user.is_authenticated:
        profile = user.profile
        sessions = models.AI_Messages.objects.filter(profile = profile)
        if sessions.exists():
            serialized = message_ai_serializer(sessions , many = True).data
            session_id = list(set([data['session_id'] for data in serialized]))
            return response.Response({'sessions':session_id},status=status.HTTP_200_OK)
        return response.Response({'sessions':[]} , status=status.HTTP_200_OK)
    raise PermissionDenied('You must be authendicated')