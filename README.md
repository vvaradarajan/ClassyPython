# DecoratorForDBReconnect
A decorator to reconnect stale db connections
Title: DB call decorator
Overview: Databasa connections become silently stale (disconnected by the DB Server, 
but status is OK on client App). The next database call ends in error. A reconnect resolves the
issue. This project is to show a python 'decorator' that resolves the re-connection, without any
changes to the DB call procedure.

The wiki contains the design of this decorator.
