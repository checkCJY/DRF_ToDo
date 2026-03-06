from django.contrib.auth.models import User
from rest_framework import serializers


# ────────────────────────────────────────────
# 회원가입 전용 Serializer
#   - ModelSerializer 대신 Serializer를 사용해
#     password2(비밀번호 확인) 필드를 직접 관리
# ────────────────────────────────────────────
class SignupSerializer(serializers.Serializer):
    # 사용자 아이디 (Django User.username 최대 길이와 동일하게 설정)
    username = serializers.CharField(max_length=150)

    # 비밀번호
    #   - write_only=True : 응답 JSON에 절대 포함되지 않음
    #   - min_length=4    : 4자 미만이면 즉시 유효성 오류 반환
    password = serializers.CharField(write_only=True, min_length=4)

    # 비밀번호 확인 (password와 동일한 값을 입력해야 함)
    password2 = serializers.CharField(write_only=True, min_length=4)

    # ── 필드 단위 검증 ──────────────────────────
    def validate_username(self, value):
        """
        username 중복 여부를 검사한다.
        DRF는 validate_<field_name> 형식의 메서드를 자동으로 호출한다.
        """
        # 동일한 username이 이미 DB에 존재하면 400 Bad Request 반환
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용중인 username 입니다.")

        return value

    # ── 객체 단위 검증 ──────────────────────────
    def validate(self, attrs):
        """
        모든 필드 검증이 끝난 뒤 호출되는 교차 검증 메서드.
        password와 password2의 일치 여부를 확인한다.
        """
        # 두 비밀번호가 다르면 password 필드 오류로 반환
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )

        return attrs

    # ── 객체 생성 ───────────────────────────────
    def create(self, validated_data):
        """
        serializer.save() 호출 시 실행되는 메서드.
        create_user()를 사용해 비밀번호를 해시(hash)처리한 뒤 저장한다.
        password2는 DB에 저장할 필요가 없으므로 전달하지 않는다.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        return user
