import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from json.decoder import JSONDecodeError
from users.models import User
from users.serializers import UsersSerializer


@csrf_exempt
def kakao_login(request):
    if request.method == 'POST':
        """
        Check Access Token & Get Email Address
        """
        headers = {
            'Authorization': request.headers['Authorization']
        }

        user_info_req = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
        user_info = user_info_req.json()

        error = user_info.get('error')
        if error is not None:
            raise JSONDecodeError(error)

        try:
            kakao_account = user_info['kakao_account']
        except KeyError:
            return JsonResponse({
                'success': False,
                'message': '유효하지 않은 액세스 토큰입니다'
            })

        email = kakao_account['email']
        username = kakao_account['profile']['nickname']
        profile_image_url = kakao_account['profile']['profile_image_url']

        try:
            user = User.objects.get(email=email)

            if profile_image_url != user.profile_image_url:
                user.profile_image_url = profile_image_url
                user.save()

        except User.DoesNotExist:
            # 기존에 가입된 유저가 없으면 새로 가입
            user = User.objects.create_user(email)
            user.username = username
            user.profile_image_url = profile_image_url
            user.save()

        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            'success': True,
            'email': email,
            'access_token': str(refresh.access_token),
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    serializer = UsersSerializer(request.user)

    response = {
        'success': True,
        'data': serializer.data
    }

    return JsonResponse(response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request, user_pk):
    try:
        user = User.objects.get(id=user_pk)
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '해당 유저를 찾을 수 없습니다'
        })

    serializer = UsersSerializer(user)

    return JsonResponse({
        'success': True,
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_by_email(request):
    email = request.GET.get('email')

    if not email:
        return JsonResponse({
            'success': False,
            'message': '이메일을 입력해주세요'
        })

    try:
        profile = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '존재하지 않는 사용자입니다'
        })

    serializer = UsersSerializer(profile)

    response = {
        'success': True,
        'data': serializer.data
    }

    return JsonResponse(response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_by_username(request):
    username = request.GET.get('username')

    if not username:
        return JsonResponse({
            'success': False,
            'message': '닉네임을 입력해주세요'
        })

    users = User.objects.filter(username=username)

    serializer = UsersSerializer(users, many=True)
    data = serializer.data

    response = {
        'success': True,
        'data': data
    }

    return JsonResponse(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_pk):
    try:
        target_user = User.objects.get(id=user_pk)
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '팔로우하려는 유저를 찾을 수 없습니다'
        })

    serializer = UsersSerializer(target_user)

    if target_user == request.user:
        return JsonResponse({
            'success': False,
            'message': '자기 자신을 팔로우할 수 없습니다'
        })

    if target_user.followers.filter(pk=request.user.pk).exists():
        target_user.followers.remove(request.user)

        return JsonResponse({
            'success': True,
            'status': 'unfollowed',
            'target': serializer.data
        })

    target_user.followers.add(request.user)

    return JsonResponse({
        'success': True,
        'status': 'followed',
        'target': serializer.data
    })
