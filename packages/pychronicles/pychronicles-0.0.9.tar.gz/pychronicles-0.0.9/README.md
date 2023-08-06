[![PyPI version](https://badge.fury.io/py/pychronicles.svg)](https://badge.fury.io/py/pychronicles)

# PyChronicle package

A chronicle is a specification of the complex temporal behaviors as a graph of temporal constraints. More specifically, a chronicle is a multiset of events and a set of temporal constraints specifying that occurrences of pairs of events must occurs within a given temporal interval.
It can be used to recognize complex behaviors in sequence the temporal events.

This library proposes a Python class to define a chronicle, to read/save them in a standard CRS format. The main useful functionnality for chronicle is their efficient matching in a temporal sequence.

A temporal sequence may have three different format:
* a simple list of items (str, int or None) with implicit timestamps : `['a', 'b', ..., None, 'c', None, 'd']`
* a list of explicitly timestamped items (str or int) : `[ (1,'a'), (23,'b'), (30,'c'), (45, 'd')]`
* a pandas dataframe indexed by timestamps and using the items in a columns (named `label`)

The chronicles handles to model of timestamps (for the last two types of sequence models):
* discrete timestamps using integers
* continuous timestamps using `datetime` format. In this case the temporal constraints of a chronicle must be defined using `timedelta` values.

The package implements efficient algorithms to recognize it. It benefits from pandas functionalities to increase their efficiency. There are three different ways to _recognize_ a chronicle in a sequence of a events:
* the absence/presence recognition (`c.match(seq)`): its result is a boolean stating whether the chronicle occur at least once in the sequence, this is the most efficient algorithm
* the occurrence enumeration (`c.recognize(seq)`): its result is a list of occurrence of the chronicle in a sequence. Contrary to the first implementation, it looks for all possible combinasion of events. Thus it is less efficient
* the approximate occurrence enumeration (`c.cmp(seq, 0.7)`): its result is a list of occurrences that are similar of the chronicle with a similarity threshold of 0.7.

In addition, when using a pandas dataframe which contains several sequences (indexed with an attribute), it is possible to request for matching a chronicle in all sequences (no specific optimisation).


Please note that the author is not fully satisfied by the function name and that it appeals to change them in a short delay ...

# Perspectives

* extend the chronicle model for pandas dataframe by specifying event by a couple (attribute, value), that can be used to specify a wider range of complex behavior in multidimensional sequences
* graphical interfaces to edit chronicle (for instance with dash)
* better cythonize the recognition
* optimized matching of several chronicles at the same time


# Requirements

Use `pip install -r requirements.txt` to install requirements.

Naturally, the latter may require superuser rights (consider prefixing the commands by sudo).

If you want to use Python 3 and your system defaults on Python 2.7, you may need to adjust the above commands, e.g., replace pip by pip3.

The required libraries are the following
* numpy
* scipy
* lazr.restfulclient
* larz.uri
* typing
* pandas

LAZR is used to instantiate chronicles from CRS files (with simple grammar).

# Usage

Example of usage:

    from pychronicles import *
    #define a sequence of events
    seq = [3,4,'b','a','a',1,3,'coucou','b','coucou',5,'coucou',5]
    
    #define a chronicle
    c=Chronicle()
    c.add_event(0,'b')
    c.add_event(1,1)
    c.add_constraint(1,3, (3,45))
    print(c)
    
    #recognize the chronicle in the sequence
    occs=c.recognize(seq)
    print("occurrences: "+str(occs))

It is possible to specify chronicles using the CRS format. The following code illustrate the syntax for specifying a chronicle in this format.

    chronicle C27_sub_0[]()
    {
	    event(Event_Type1[], t006)
	    event(Event_Type1[], t004)
	    event(Event_Type2[], t002)
	    event(Event_Type3[], t001)

	    t004-t006 in [17,25]
	    t006-t002 in [-16,-10]
	    t002-t001 in [14,29]
	    t004-t001 in [27,35]
    }


# Authorship

* **Author:** Thomas Guyet
* **Institution:** Inria
* **date:** 8/2022

