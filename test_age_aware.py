#!/usr/bin/env python3
"""Test script for age-aware chronological route."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from api.routes import ChronologicalSteward


def test_age_aware_phases():
    """Test that phases are correctly filtered by age range."""
    print("="*60)
    print("Testing Age-Aware Phase Progression")
    print("="*60)
    
    # Test each age range
    age_ranges = [
        ("1", "under_18", ["GREETING", "AGE_SELECTION", "CHILDHOOD", "ADOLESCENCE", "PRESENT", "SYNTHESIS"]),
        ("2", "18_30", ["GREETING", "AGE_SELECTION", "CHILDHOOD", "ADOLESCENCE", "EARLY_ADULTHOOD", "PRESENT", "SYNTHESIS"]),
        ("3", "31_45", ["GREETING", "AGE_SELECTION", "CHILDHOOD", "ADOLESCENCE", "EARLY_ADULTHOOD", "MIDLIFE", "PRESENT", "SYNTHESIS"]),
        ("4", "46_60", ["GREETING", "AGE_SELECTION", "CHILDHOOD", "ADOLESCENCE", "EARLY_ADULTHOOD", "MIDLIFE", "PRESENT", "SYNTHESIS"]),
        ("5", "61_plus", ["GREETING", "AGE_SELECTION", "CHILDHOOD", "ADOLESCENCE", "EARLY_ADULTHOOD", "MIDLIFE", "PRESENT", "SYNTHESIS"]),
    ]
    
    for age_num, age_key, expected_phases in age_ranges:
        print(f"\n📊 Testing age range {age_num}: {age_key}")
        
        # Create route instance
        route = ChronologicalSteward()
        
        # Simulate greeting phase
        route.phase = "GREETING"
        assert route.should_advance("yes"), f"Should advance from GREETING on 'yes'"
        
        # Simulate age selection
        route.phase = "AGE_SELECTION"
        assert route.should_advance(age_num), f"Should advance from AGE_SELECTION on '{age_num}'"
        
        # Verify age range was set
        assert route.age_range == age_key, f"Age range should be {age_key}, got {route.age_range}"
        
        # Verify phase order matches expected
        assert route.phase_order == expected_phases, f"Phase order mismatch!\nExpected: {expected_phases}\nGot: {route.phase_order}"
        
        print(f"   ✅ Age range set correctly: {age_key}")
        print(f"   ✅ Phase order configured: {len(route.phase_order)} phases")
        print(f"   ✅ Phases: {', '.join(route.phase_order[2:])}")  # Skip GREETING and AGE_SELECTION
    
    print("\n" + "="*60)
    print("✅ All age-aware phase tests passed!")
    print("="*60)


def test_route_metadata():
    """Test route info includes presentation field."""
    print("\n" + "="*60)
    print("Testing Route Metadata")
    print("="*60)
    
    route = ChronologicalSteward()
    info = route.route_info
    
    print(f"\n📋 Route Name: {info['name']}")
    print(f"🎯 Goal: {info['goal']}")
    print(f"📖 Presentation: {info['presentation']}")
    
    assert "presentation" in info, "Route info should include 'presentation' field"
    assert "chronologically" in info["presentation"].lower(), "Presentation should mention chronological organization"
    
    print("\n✅ Route metadata test passed!")
    print("="*60)


def test_phase_instructions():
    """Test that AGE_SELECTION phase has proper instructions."""
    print("\n" + "="*60)
    print("Testing Phase Instructions")
    print("="*60)
    
    route = ChronologicalSteward()
    
    # Check AGE_SELECTION phase exists
    assert "AGE_SELECTION" in route.interview_phases, "AGE_SELECTION phase should exist"
    
    age_phase = route.interview_phases["AGE_SELECTION"]
    instruction = age_phase["system_instruction"]
    
    print(f"\n📝 AGE_SELECTION instruction preview:")
    print(f"   {instruction[:150]}...")
    
    # Verify instruction contains age range options
    assert "1-5" in instruction or "1" in instruction and "5" in instruction, "Should mention age options 1-5"
    assert "Under 18" in instruction or "under 18" in instruction, "Should mention 'Under 18' option"
    assert "61" in instruction, "Should mention '61 and above' option"
    
    print("\n✅ Phase instruction test passed!")
    print("="*60)


if __name__ == "__main__":
    try:
        test_age_aware_phases()
        test_route_metadata()
        test_phase_instructions()
        
        print("\n" + "🎉"*30)
        print("ALL TESTS PASSED! Age-aware system is working correctly.")
        print("🎉"*30 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
