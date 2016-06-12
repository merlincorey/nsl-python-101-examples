#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
merlin-nsl-adventure

  It's dark and you're trapped in a room.  There's no way out... or is there?

  Find out in this single room adventure game complete with online help.

  For you younguns, online means available within the program command line.

This program is meant to demonstrate a highly "functional" methodology of programming.
It uses only core python features and libraries and is a "complete" game.
'''

import random
import sys

def print_header_items(header, items, per_item='* {}', delimiter='\n'):
    print header
    print delimiter.join(per_item.format(item) for item in items)


def command_unknown(data, pieces):
    print 'Unrecognized command: {}'.format(pieces[0])
    return data


def command_help(data, pieces):
    print_header_items('Commands:', data['commands'])
    return data


def command_inventory(data, pieces):
    print_header_items('Inventory:', data['inventory'])
    return data


def command_dingdingding(data, pieces):
    data['win'] = True
    data['inventory'].append('black badge')
    return data


def command_look(data, pieces):
    print 'It is {} lit in here'.format(data['lit'] and 'brightly' or 'dimly')
    if 1 == len(pieces):
        print_header_items('Objects in room:', data['lit'] and data['objects'] or [d for d in data['objects'] if d in ('lamp', 'door')])
    else:
        if pieces[1] in data['objects']:
            print 'Looking at {}...'.format(pieces[1])
            if 'lamp' == pieces[1]:
                print 'The lamp is {}'.format(data['lit'] and 'on and hurt your eyes' or 'off')
            elif 'door' == pieces[1]:
                print 'The door is large, metal, and closed.'
            elif 'chair' == pieces[1]:
                if data['lit']:
                    print 'The chair is green and black upholstery and looks very comfortable.'
                else:
                    print 'There appears to be a lumpy chair in the corner of the room.'
            elif 'lockpicks' == pieces[1]:
                if data['lit']:
                    print 'You see a small southard case with some basic lockpicks and tension wrenches.'
                else:
                    print 'You cannot see anything like that.'
            elif 'whistle' == pieces[1]:
                if data['lit']:
                    print 'You see a small, red whistle.'
                else:
                    print 'You cannot see anything like that.'
        else:
            print 'You must be hallucinating, because thats not there.'
    return data


def command_use(data, pieces):
    if 1 == len(pieces):
        print 'You must use an object!'
    else:
        if pieces[1] in data['objects']:
            print 'Using the {}...'.format(pieces[1])
            if 'lamp' == pieces[1]:
                data['lit'] = not data['lit']
                print 'The lamp is now {}'.format(data['lit'] and 'on' or 'off')
            elif 'lockpicks' == pieces[1]:
                if 'lockpicks' in data['inventory']:
                    print 'Trying to use the lockpicks.'
                    data['attempts'] += 1
                    if 0 == random.randint(0, 5 * (data['lit'] and 1 or 2)):
                        print 'CLICK!'
                        print 'The lock is opened.'
                        data['locked'] = False
                    else:
                        print 'The lock {}!'.format(random.choice(['resists', 'resists', 'resists', 'fights back', 'bites']))
                else:
                    print 'You have not picked up any lockpicks.'
            elif 'whistle' == pieces[1]:
                if 'whistle' in data['inventory']:
                    print 'You blow the whistle and make a shrill sound.'
                else:
                    print 'You have not picked up any whistles.'
            elif 'chair' == pieces[1]:
                print 'You sit down in the chair.'
                print
                print 'After a few minutes you stand up, refreshed.'
            elif 'door' == pieces[1]:
                if data['locked']:
                    print 'The door is locked.'
                else:
                    print 'The door is open.'
                    data['win'] = True
    return data


def command_pickup(data, pieces):
    if 1 == len(pieces):
        print 'You must pickup an object!'
    else:
        if pieces[1] in data['objects']:
            print 'Picking up the {}...'.format(pieces[1])
            if 'lamp' == pieces[1]:
                print 'The lamp is light and easily moved.'
                print 'You set it down a few inches away.'
            elif 'lockpicks' == pieces[1]:
                if 'lockpicks' in data['inventory']:
                    print 'You already have the lockpicks!'
                else:
                    print 'You pick up the lockpicks.'
                    data['inventory'].append('lockpicks')
            elif 'whistle' == pieces[1]:
                if 'whistle' in data['inventory']:
                    print 'You already have the whistle!'
                else:
                    print 'You pick up the whistle.'
                    data['inventory'].append('whistle')
            elif 'chair' == pieces[1]:
                print 'The chair is cemented to the floor!  You dont seem to have a drill.'
            elif 'door' == pieces[1]:
                print 'The door does not budge.'
        else:
            print 'Nothing like that around here!'
    return data


def command_drop(data, pieces):
    if 1 == len(pieces):
        print 'You must drop an object!'
    else:
        if pieces[1] in data['inventory']:
            print 'Dropping the {}...'.format(pieces[1])
            data['inventory'].remove(pieces[1])
            print 'You dropped the {}.'.format(pieces[1])
        else:
            print 'You are not holding anything like that.'
    return data


def find_command(command_name, default, prefix='command_'):
    command = default
    for c in (f for n, f in globals().iteritems() if callable(f) and n.startswith(prefix)):
        if command_name == c.__name__.rpartition(prefix)[2]:
            command = c
            break
    return command


def filter_useless_words(seq, useless=['a', 'an', 'at', 'the', 'damn', 'shitty', 'fucking', 'lame', 'sweet']):
    return [x for x in seq if x not in useless]


def execute_command(data, pieces):
    command = find_command(pieces[0], default=command_unknown)
    data['inputs'] += 1
    return command(data, filter_useless_words(pieces))


def game_won(data):
    print 'YOU WON THE GAME!\nYOU ARE AMAZING!\nYOU DID THE THINGS!\n' * 3
    print 'After {} commands, and {} lockpicking attempts, you have gotten free from THE ROOM!'.format(data['inputs'], data['attempts'])
    print
    command_inventory(data, [])


def game_step(data):
    try:
        print
        command = raw_input('adventure> ')
    except (EOFError, KeyboardInterrupt), e:
        print
        print 'Exiting!'
        command = 'exit'
    running = not command.lower().startswith('exit')
    if running:
        print
        pieces = command.split()
        data = execute_command(data, pieces)
        if data['win']:
            game_won(data)
            running = False
    return running


def game_loop():
    running = True
    while running:
        data = {'objects':['chair', 'door', 'lockpicks', 'lamp', 'whistle'],
                'commands':['help', 'look', 'use', 'pickup', 'drop', 'inventory'],
                'chair':'h',
                'inventory':[],
                'attempts':0,
                'inputs':0,
                'lit':False,
                'locked':True,
                'win':False}
        while running:
            running = game_step(data)


def main():
    print 'Try using the "help" command to get a list of available commands.'
    game_loop()

    """# Original example program from the class before "expanding"
    print '=' * 30
    print 'Welcome to my Awesome Program!'
    print '=' * 30
    
    print
    a = raw_input('What is your name? ')
    print 'Your name is: {}'.format(a)

    print
    b = raw_input('Are you ready for an adventure? ')
    print
    if 'yes' == b.lower():
        print 'ADVENTURE TIME\n' * 5
    else:
        print 'FINE BE THAT WAY'
    """

    print
    return 0

if '__main__' == __name__:
    sys.exit(main())
