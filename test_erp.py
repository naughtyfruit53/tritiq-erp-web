#!/usr/bin/env python3
"""
Basic test script to verify the FastAPI ERP application is working correctly.
This tests the core functionality including database connectivity, API endpoints, and basic CRUD operations.
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.db.session import get_db_context
from src.db.crud.users import get_users, create_user
from src.db.crud.company_details import get_company_detail
from src.db.crud.voucher_types import get_voucher_types
from src.db.schemas.users import UserCreate

async def test_database_connectivity():
    """Test basic database connectivity"""
    print("🔍 Testing database connectivity...")
    try:
        async with get_db_context() as db:
            # Simple query to test connection
            voucher_types = await get_voucher_types(db)
            print(f"✅ Database connected successfully! Found {len(voucher_types)} voucher types.")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

async def test_user_operations():
    """Test user CRUD operations"""
    print("👤 Testing user management...")
    try:
        async with get_db_context() as db:
            # Get existing users
            users = await get_users(db)
            print(f"✅ Found {len(users)} existing users")
            
            # Check if we can create a test user (if no admin exists)
            if len(users) == 0:
                test_user = UserCreate(username="test_admin", password="test123", is_admin=True)
                new_user = await create_user(db, test_user)
                print(f"✅ Created test user: {new_user.username}")
            
            return True
    except Exception as e:
        print(f"❌ User operations failed: {e}")
        return False

async def test_voucher_system():
    """Test voucher type system"""
    print("📜 Testing voucher system...")
    try:
        async with get_db_context() as db:
            voucher_types = await get_voucher_types(db)
            
            # Check for essential voucher types
            expected_types = ['sales_order', 'purchase_order', 'quotation', 'grn']
            found_types = [vt.module_name for vt in voucher_types]
            
            missing_types = [t for t in expected_types if t not in found_types]
            if missing_types:
                print(f"⚠️ Missing voucher types: {missing_types}")
            
            print(f"✅ Voucher system working. Available types: {len(voucher_types)}")
            for vt in voucher_types:
                print(f"   - {vt.name} ({vt.module_name})")
            
            return True
    except Exception as e:
        print(f"❌ Voucher system test failed: {e}")
        return False

async def test_company_setup():
    """Test company details functionality"""
    print("🏢 Testing company setup...")
    try:
        async with get_db_context() as db:
            company = await get_company_detail(db)
            if company:
                print(f"✅ Company setup found: {company.company_name}")
            else:
                print("ℹ️ No company details configured yet (expected for new installation)")
            return True
    except Exception as e:
        print(f"❌ Company setup test failed: {e}")
        return False

async def run_all_tests():
    """Run all tests and report results"""
    print("🚀 Starting Tritiq ERP Application Tests")
    print("="*50)
    
    tests = [
        ("Database Connectivity", test_database_connectivity),
        ("User Operations", test_user_operations),
        ("Voucher System", test_voucher_system),
        ("Company Setup", test_company_setup),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! The ERP application is ready for use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the application configuration.")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)