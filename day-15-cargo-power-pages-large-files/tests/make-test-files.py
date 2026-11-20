"""Create dummy files to test each limit (not committed: they're big). Usage: python make-test-files.py"""
import os
for name, mb in [("04MB.pdf", 4), ("12MB.pdf", 12), ("80MB.zip", 80), ("120MB.zip", 120), ("600MB.mp4", 600), ("bad-type.exe", 1)]:
    with open(name, "wb") as f: f.truncate(mb * 1024 * 1024)  # sparse file of the right size
    print("created", name)
