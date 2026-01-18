#!/usr/bin/env python3
# main.py

import sys
sys.dont_write_bytecode = True

from examples import (
    example_scale, 
    example_twinkle_star,
    example_chords,
    example_overlapping_voices, 
    example_drums,
    example_multiple_tracks
)

def main():
    tests = [
        example_scale, 
        example_twinkle_star,
        example_chords,
        example_overlapping_voices, 
        example_drums,
        example_multiple_tracks
    ]

    for test in tests:
        test_name = test.__name__
        print("Testing {} ...".format(test_name))
        test()
        print("Testing {} - good.".format(test_name))
        print()

    print("All tests passed.")

if __name__ == "__main__":
    main()

