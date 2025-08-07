Server Management
=================

User request approved -> assign reservation time slot -> User accesses system.

.. mermaid::

   graph LR;
       A[User request approved] --> B[assign reservation time slot];
       B --> C[User accesses system];

.. _setcomputealias:

Set Compute Alias
-----------------

.. _setcomputestatus:

Set Compute Status
------------------

System status is an attribute that defines how a compute resource is presented to the portal.
0 - System is not available from the public reservation pool and manual reservation assignment is not available.
1 - System is available in the public reservation pool and for manual reservation assignment.
2 - System is not available in the public reservation pool but is available for manual reservation assignment.

Use status 0 when:
- 

Manually Start Reserveration for a User
---------------------------------------
