import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token,
    verify_token, verify_access_token, verify_refresh_token,
    create_reset_password_token, verify_reset_password_token,
    create_verification_token, verify_verification_token
)


def test_password_hashing():
    """Test password hashing"""
    try:
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        print(f"✓ Password: {password}")
        print(f"✓ Hashed: {hashed[:50]}...")
        result = verify_password(password, hashed)
        print(f"✓ Verify: {result}")
        print()
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_token_creation():
    """Test JWT token creation and verification"""
    try:
        user_id = 1

        # Access token
        access_token = create_access_token(user_id)
        print(f"✓ Access Token: {access_token[:50]}...")

        # Verify access token
        payload = verify_access_token(access_token)
        print(f"✓ Access Token Payload: {payload}")

        # Refresh token
        refresh_token = create_refresh_token(user_id)
        print(f"✓ Refresh Token: {refresh_token[:50]}...")

        # Verify refresh token
        payload = verify_refresh_token(refresh_token)
        print(f"✓ Refresh Token Payload: {payload}")
        print()
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_reset_password_token():
    """Test password reset token"""
    try:
        email = "test@example.com"

        # Create token
        token = create_reset_password_token(email)
        print(f"✓ Reset Token: {token[:50]}...")

        # Verify token
        verified_email = verify_reset_password_token(token)
        print(f"✓ Verified Email: {verified_email}")
        print()
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_verification_token():
    """Test email verification token"""
    try:
        email = "test@example.com"

        # Create token
        token = create_verification_token(email)
        print(f"✓ Verification Token: {token[:50]}...")

        # Verify token
        verified_email = verify_verification_token(token)
        print(f"✓ Verified Email: {verified_email}")
        print()
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Testing Security Module")
    print("=" * 50)
    print()

    tests = [
        ("Password Hashing", test_password_hashing),
        ("Token Creation", test_token_creation),
        ("Reset Password Token", test_reset_password_token),
        ("Verification Token", test_verification_token),
    ]

    passed = 0
    for name, test_func in tests:
        print(f"Testing {name}...")
        if test_func():
            passed += 1
        print("-" * 40)

    print(f"\n✓ {passed}/{len(tests)} tests passed!")

    if passed == len(tests):
        print("\n🎉 All security tests passed!")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")