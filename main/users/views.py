from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from rest_framework.exceptions import ValidationError


# Create your views here.
class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'user':serializer.data, 'message': 'Logged in successfully', 'success': True})
        except ValidationError as err:
            errorMessage = err.detail
            return Response({'success': False, 'message': errorMessage})
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        
        if user is None:
            return Response({'success': False, 'message': 'User not found'})
        
        if not user.check_password(password):
            return Response({'success': False, 'message': 'Wrong password'})

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'madrid', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True, samesite=None, domain="http://localhost:3000")
        response.data = {
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'rating':user.rating,
                'jwt': token,
            },
            'success': True,
            'message': 'Logged in successfully'
        }
        return response


class UserView(APIView):

    def get(self, request):
        # Get the JWT token from cookies
        token = request.headers.get('Authorization')
        
        if not token:
            return Response({'success': False, 'message': 'Unauthenticated!'})

        try:
            # Decode the token
            payload = jwt.decode(token, 'madrid', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! Token has expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Unauthenticated! Invalid token.')

        # Fetch user based on the ID from the token
        user = User.objects.filter(id=payload['id']).first()

        if not user:
            return Response({'success': False, 'message': 'User not found'})

        # Serialize the user data
        serializer = UserSerializer(user)
        return Response({'success': True, 'user': serializer.data})

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'success': True,
            'message': 'success'
        }
        return response