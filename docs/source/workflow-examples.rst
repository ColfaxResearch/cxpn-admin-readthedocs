Workflow Examples
=================

Step-by-step workflows with UI diagrams for common admin tasks.

User Management
---------------

How to Approve a User Access Request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow covers approving a new user's registration request in the admin panel.

.. mermaid::

   graph TD
       A[Navigate to Manage Requests] --> B[Find PENDING request]
       B --> C[Click Review]
       C --> D[Click Approve]
       D --> E[Status: APPROVED]

Steps:

1. Navigate to **User Registration > Manage Requests** in the admin panel. The new request appears with status ``PENDING``.
2. Click **Review** to inspect the full registration details, including all submitted metadata fields.
3. Click **Approve** to grant the user access. The request status changes to ``APPROVED`` and the user receives an approval email.

How to Add a User Manually
~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow covers manually creating a new user registration entry in the admin panel, bypassing the public registration form. This is useful when onboarding users directly or when the public form is unavailable.

.. mermaid::

   graph TD
       A[Navigate to Manage Requests] --> B[Click Add New User]
       B --> C[Fill in user details]
       C --> D[Set request status]
       D --> E[Click Save]
       E --> F[User added to table]

Steps:

1. Navigate to **User Registration > Manage Requests** in the admin panel.
2. Click **Add New User** to open the manual registration form.
3. Fill in the user's details:
   - **Email Address** -- The user's email address
   - **First Name** -- The user's first name
   - **Last Name** -- The user's last name
   - **Organization** -- The user's organization or company
   - **Country** -- The user's country
   - **Purpose** -- The reason for the user's access request
4. Set the **Request Status** to ``PENDING`` (for admin review later) or ``APPROVED`` (to grant immediate access).
5. Click **Save**. The user entry is added to the Manage Requests table with the specified status.
6. If set to ``APPROVED``, the user's project access is provisioned immediately and they receive an approval email. If set to ``PENDING``, the entry awaits review like a normal registration request.

How to Remove a User
~~~~~~~~~~~~~~~~~~~~

This workflow covers terminating a user's access to the test drive portal.

.. mermaid::

   graph TD
       A[Navigate to Project Access] --> B[Find user in table]
       B --> C[Click End Access]
       C --> D[Access terminated]

Steps:

1. Navigate to **Project Management > Project Access** in the admin panel.
2. Locate the user in the table and click **End Access**.
3. The user's access is deactivated and any active reservations are invalidated. The user receives a deactivation email.

How to Extend a User's Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow covers extending a user's project access period beyond the default duration.

.. mermaid::

   graph TD
       A[Navigate to Project Access] --> B[Find user in table]
       B --> C[Click Edit]
       C --> D[Set new End Date]
       D --> E[Click Update]
       E --> F[Access extended]

Steps:

1. Navigate to **Project Management > Project Access** in the admin panel.
2. Locate the user and click **Edit** (Quick Edit).
3. In the quick edit form, modify the **End Date** to the desired new date and time.
4. Click **Update**. The override takes precedence over the default access period.

How to Override a User's Reservation Duration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow covers changing the reservation duration for a specific user.

.. mermaid::

   graph TD
       A[Navigate to Manage Requests] --> B[Find user in table]
       B --> C[Click Edit]
       C --> D[Set new Reservation Duration]
       D --> E[Click Update]
       E --> F[Duration updated]

Steps:

1. Navigate to **User Registration > Manage Requests** or **Project Management > Project Access**.
2. Locate the user and click **Edit** (Quick Edit).
3. In the quick edit form, modify the **Reservation Duration** field to the desired number of hours.
4. Click **Update**. The change applies to all future reservations made by the user.

How to Invite a User via Instant Access Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow covers creating an instant access code for an event.

.. mermaid::

   graph TD
       A[Navigate to Instant Access Codes] --> B[Click Add New]
       B --> C[Fill in code details]
       C --> D[Click Save]
       D --> E[Code created]
       E --> F[Distribute code to users]

Steps:

1. Navigate to **User Registration > Instant Access Codes** and click **Add New**.
2. Fill in the code details including event name, validity period, access period, reservation duration, hardware group, max users, whitelisted domains, and description.
3. Click **Save**. The code is now active and can be distributed to event attendees.
4. When a user enters the code on the registration form, their request is auto-approved.

How to Change a User's Hardware Group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow covers modifying the hardware group assigned to an existing user.

.. mermaid::

   graph TD
       A[Navigate to Project Access] --> B[Find user in table]
       B --> C[Click Edit]
       C --> D[Select new Hardware Group]
       D --> E[Click Update]
       E --> F[Group updated]

Steps:

1. Navigate to **Project Management > Project Access**.
2. Locate the user and click **Edit** (Quick Edit).
3. In the quick edit form, modify the **Hardware Group** field to the desired group.
4. Click **Update**. The change takes effect for the user's next reservation.

How to Reject a Registration Request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow covers denying a pending registration request.

.. mermaid::

   graph TD
       A[Navigate to Manage Requests] --> B[Find PENDING request]
       B --> C[Click Review]
       C --> D[Click Reject]
       D --> E[Status: REJECTED]

Steps:

1. Navigate to **User Registration > Manage Requests**.
2. Locate the pending request and click **Review** to inspect the details.
3. Click **Reject** to deny the registration. The request status changes to ``REJECTED`` and the user receives a rejection email.
