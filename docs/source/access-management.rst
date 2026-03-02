Access Management
=================

User request approved -> assign reservation time slot -> User accesses system.

.. mermaid::

   graph LR;
       A[User request approved] --> B[assign reservation time slot];
       B --> C[User accesses system];

.. _inviteusers:

Invite Users
------------

..
   To use Lumache, first install it using pip:

   .. code-block:: console

      (.venv) $ pip install lumache


.. _removeusers:

Remove Users
------------

..
   To retrieve a list of random ingredients,
   you can use the ``lumache.get_random_ingredients()`` function:

   .. autofunction:: lumache.get_random_ingredients

   The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
   or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`
   will raise an exception.

   .. autoexception:: lumache.InvalidKindError

   For example:

   >>> import lumache
   >>> lumache.get_random_ingredients()
   ['shells', 'gorgonzola', 'parsley']


Manually Start Reserveration for a User
---------------------------------------

Set Non-default User Project Access Duration
--------------------------------------------

Use this workflow when a user needs a project access period that differs from the project default.

1. Open the Admin portal and navigate to the Colfax Connect plug-in using the left side-bar. In the main pane, navigate to the `Project Access` tab in the `Project Management` section.
2. Find the user whose access end date you would like to override and click `Edit`.
3. In the quick edit menu, select the appropriate `End date` date and time.
4. Save the assignment changes by clicking `Update`.

Notes:
   - The user-project override takes precedence over the project default duration.

Set Non-default User Server Reservation Duration
------------------------------------------------

Use this workflow when a user needs a reservation duration that differs from the default reservation duration.
