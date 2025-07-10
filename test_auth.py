#!/usr/bin/env python3
"""
Simple test script to verify the authentication system setup.
This script checks if all required modules can be imported and basic functionality works.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import firebase_admin
        print("✅ firebase-admin imported successfully")
    except ImportError as e:
        print(f"❌ firebase-admin import failed: {e}")
        return False
    
    try:
        import jwt
        print("✅ PyJWT imported successfully")
    except ImportError as e:
        print(f"❌ PyJWT import failed: {e}")
        return False
    
    try:
        from app.auth.models import UserSignupRequest, UserLoginRequest
        print("✅ Auth models imported successfully")
    except ImportError as e:
        print(f"❌ Auth models import failed: {e}")
        return False
    
    try:
        from app.auth.firebase_auth import FirebaseAuthService
        print("✅ Firebase auth service imported successfully")
    except ImportError as e:
        print(f"❌ Firebase auth service import failed: {e}")
        return False
    
    try:
        from app.auth.dependencies import get_current_user
        print("✅ Auth dependencies imported successfully")
    except ImportError as e:
        print(f"❌ Auth dependencies import failed: {e}")
        return False
    
    try:
        from app.main import app
        print("✅ FastAPI app imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI app import failed: {e}")
        return False
    
    return True


def test_environment_variables():
    """Test if required environment variables are set"""
    print("\nTesting environment variables...")
    
    required_vars = [
        "JWT_SECRET",
        "FIREBASE_CREDENTIALS",
        "FIREBASE_SERVICE_ACCOUNT_PATH"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("   These are required for full functionality")
        return False
    else:
        print("✅ All required environment variables are set")
        return True


def test_fastapi_app():
    """Test if FastAPI app can be created"""
    print("\nTesting FastAPI app...")
    
    try:
        from app.main import app
        routes = [route.path for route in app.routes]
        print(f"✅ FastAPI app created successfully with {len(routes)} routes")
        
        # Check for auth routes
        auth_routes = [route for route in routes if route.startswith('/auth')]
        print(f"✅ Found {len(auth_routes)} authentication routes")
        
        return True
    except Exception as e:
        print(f"❌ FastAPI app test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🔍 Testing Authentication System Setup\n")
    
    tests = [
        test_imports,
        test_environment_variables,
        test_fastapi_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The authentication system is ready to use.")
        print("\nNext steps:")
        print("1. Configure your Firebase project")
        print("2. Set up environment variables in .env file")
        print("3. Run: python run.py")
        print("4. Visit: http://localhost:8000/docs")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main() 
