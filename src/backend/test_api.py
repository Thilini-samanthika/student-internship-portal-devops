
Simple API test script for GitHub Actions
Tests basic API endpoints without external dependencies

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    try:
        from flask import Flask
        from flask_cors import CORS
        from flask_jwt_extended import JWTManager
        from werkzeug.security import generate_password_hash
        import mysql.connector
        print(" All imports successful")
        return True
    except ImportError as e:
        print(f" Import error: {e}")
        return False

def test_app_creation():
    """Test if Flask app can be created"""
    try:
        # Import app after setting up test environment
        os.environ['TESTING'] = 'True'
        from backend.app import app
        assert app is not None
        assert app.config['JWT_SECRET_KEY'] is not None
        print("✓ Flask app creation successful")
        return True
    except Exception as e:
        print(f"✗ App creation error: {e}")
        return False

def test_password_hashing():
    """Test password hashing functionality"""
    try:
        from werkzeug.security import generate_password_hash, check_password_hash
        password = "test123"
        hashed = generate_password_hash(password)
        assert check_password_hash(hashed, password)
        assert not check_password_hash(hashed, "wrong_password")
        print(" Password hashing works correctly")
        return True
    except Exception as e:
        print(f" Password hashing error: {e}")
        return False

def main():
    """Run all tests"""
    print("Running API tests...")
    print("-" * 50)
    
    tests = [
        test_imports,
        test_app_creation,
        test_password_hashing
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f" Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("-" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print(" All tests passed!")
        sys.exit(0)
    else:
        print(" Some tests failed")
        sys.exit(1)

if __name__ == '__main__':
    main()

