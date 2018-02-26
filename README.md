# ClassyPython
This is a collection of python solutions for unique problems:

## A decorator to reconnect stale db connections
Title: DB call decorator
Overview: Databasa connections become silently stale (disconnected by the DB Server, 
but status is OK on client App). The next database call ends in error. A reconnect resolves the
issue. This project is to show a python 'decorator' that resolves the re-connection, without any
changes to the DB call procedure.

The wiki contains the design of this decorator.

## Json Algebra
Title: Json Algebra
Overview: Often multiple Json objects needs to be consolidated into a single Json. This class jsonAlgebra is a collection of two such consolidation methods. The first one is resolving Json dependencies, via a 'dotted' notation dependency specification.  The second is an 'addition' of multiple Json objects into a single one. Introduction of such algebra, should result in simplification of problems such as modular configuration, creation of comprehensive JSON from multiple sources etc.

