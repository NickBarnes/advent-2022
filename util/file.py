# Boilerplate to support Advent of Code hackery
import sys
import os

def files(file = None):
    if len(sys.argv) > 1:
        return sys.argv[1:]
    else:
        return os.path.join(file, 'input.txt')

def lines(filename):
    return [l.strip() for l in open(filename,'r') if l]

def sections(filename):
    return [[l.strip() for l in s.strip().split('\n')]
            for s in open(filename,'r').read().split('\n\n')]

def words(filename):
    return [l.strip().split() for l in open(filename,'r') if l]

def digit_grid(lines):
    return [[int(c) for c in l.strip()] for l in lines]

def digits(filename):
    return digit_grid(lines(filename))

def char_grid(lines):
    return [[c for c in l.strip()] for l in lines]

def chars(filename):
    return char_grid(lines(filename))

