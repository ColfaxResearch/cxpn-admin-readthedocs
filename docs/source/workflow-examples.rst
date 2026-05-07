Workflow Examples
=================

Step-by-step workflows with sequence diagrams for common admin tasks.

User Management
---------------

How to Add a User
~~~~~~~~~~~~~~~~~

This workflow covers adding a new user through the public registration form and approving their request in the admin panel.

.. mermaid::

   sequenceDiagram
       participant U as User
       participant P as Portal
       participant A as Admin
       participant D as Colfax DB API

       U->>P: Submits registration form
       P->>P: Validates (reCAPTCHA, email, blacklist)
       P->>A: Notifies admin via email
       A->>P: Navigates to Manage Requests
       P-->>A: Shows PENDING request
       A->>P: Clicks Review
       P-->>A: Displays full details
       A->>P: Clicks Approve
       P->>D: Provisions project access
       D-->>P: Access provisioned
       P->>U: Sends approval email
       P-->>A: Request status: APPROVED

Steps:

1. The user submits a registration request through the public-facing form. The portal validates the submission (reCAPTCHA, email format, blacklisted domains, duplicate check).
2. The admin receives an email notification of the new registration.
3. Navigate to **User Registration > Manage Requests** in the admin panel. The new request appears with status ``PENDING``.
4. Click **Review** to inspect the full registration details, including all submitted metadata fields.
5. Click **Approve** to provision the user's project access. The portal calls the Colfax DB API to create the access record.
6. The user receives an approval email, and the request status changes to ``APPROVED``.

How to Remove a User
~~~~~~~~~~~~~~~~~~~~

This workflow covers terminating a user's access to the test drive portal.

.. mermaid::

   sequenceDiagram
       participant A as Admin
       participant P as Portal
       participant D as Colfax DB API
       participant U as User

       A->>P: Navigates to Project Access
       P-->>A: Lists all users with access
       A->>P: Locates user, clicks End Access
       P->>D: Deactivates project access
       D-->>P: Access deactivated
       P->>U: Sends deactivation email
       P-->>A: Access terminated

Steps:

1. Navigate to **Project Management > Project Access** in the admin panel.
2. Locate the user in the table and click **End Access**.
3. The portal calls the Colfax DB API to deactivate the user's access. Any active reservations associated with that access are invalidated.
4. The user receives a deactivation email, and the access is terminated immediately.

How to Extend a User's Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow covers extending a user's project access period beyond the default duration.

.. mermaid::

   sequenceDiagram
       participant A as Admin
       participant P as Portal
       participant D as Colfax DB API

       A->>P: Navigates to Project Access
       P-->>A: Lists all users with access
       A->>P: Clicks Edit on user entry
       P-->>A: Shows quick edit form
       A->>P: Sets new End Date, clicks Update
       P->>D: Updates access end date
       D-->>P: Access updated
       P-->>A: Confirmation

Steps:

1. Navigate to **Project Management > Project Access** in the admin panel.
2. Locate the user and click **Edit** (Quick Edit).
3. In the quick edit form, modify the **End Date** to the desired new date and time.
4. Click **Update**. The portal calls the Colfax DB API to update the access record.
5. The override takes precedence over the default access period and is reflected immediately.

How to Override a User's Reservation Duration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow covers changing the reservation duration for a specific user.

.. mermaid::

   sequenceDiagram
       participant A as Admin
       participant P as Portal
       participant D as Colfax DB API

       A->>P: Navigates to Manage Requests
       P-->>A: Lists all registration requests
       A->>P: Clicks Edit on user entry
       P-->>A: Shows quick edit form
       A->>P: Sets new Reservation Duration, clicks Update
       P->>D: Updates reservation duration
       D-->>P: Duration updated
       P-->>A: Confirmation

Steps:

1. Navigate to **User Registration > Manage Requests** or **Project Management > Project Access**.
2. Locate the user and click **Edit** (Quick Edit).
3. In the quick edit form, modify the **Reservation Duration** field to the desired number of hours.
4. Click **Update**. The change applies to all future reservations made by the user.

How to Invite a User via Instant Access Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow covers creating an instant access code for an event and tracking its usage.

.. mermaid::

   sequenceDiagram
       participant A as Admin
       participant P as Portal
       participant U as User
       participant D as Colfax DB API

       A->>P: Navigates to Instant Access Codes
       A->>P: Clicks Add New, fills code details
       P-->>A: Code created
       U->>P: Submits registration with access code
       P->>P: Validates code (window, usage, domain)
       P->>P: Auto-approves registration
       P->>D: Provisions project access
       D-->>P: Access provisioned
       P->>U: Sends approval email
       P-->>P: Increments usage_count

Steps:

1. Navigate to **User Registration > Instant Access Codes** and click **Add New**.
2. Fill in the code details (event name, validity period, access period, reservation duration, hardware group, max users, whitelisted domains, description).
3. Distribute the code to event attendees.
4. When a user enters the code on the registration form, the portal validates it (validity window, usage count, email domain whitelist).
5. If valid, the registration is auto-approved, access is provisioned via the Colfax DB API, and the user receives an approval email.
6. The code's ``usage_count`` increments with each redemption.

How to Change a User's Hardware Group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow covers modifying the hardware group assigned to an existing user.

.. mermaid::

   sequenceDiagram
       participant A as Admin
       participant P as Portal
       participant D as Colfax DB API

       A->>P: Navigates to Project Access
       P-->>A: Lists all users with access
       A->>P: Clicks Edit on user entry
       P-->>A: Shows quick edit form
       A->>P: Selects new Hardware Group, clicks Update
       P->>D: Updates hardware group assignment
       D-->>P: Assignment updated
       P-->>A: Confirmation

Steps:

1. Navigate to **Project Management > Project Access**.
2. Locate the user and click **Edit** (Quick Edit).
3. In the quick edit form, modify the **Hardware Group** field to the desired group.
4. Click **Update**. The change takes effect immediately for the user's next reservation.

How to Reject a Registration Request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow covers denying a pending registration request.

.. mermaid::

   sequenceDiagram
       participant A as Admin
       participant P as Portal
       participant U as User

       A->>P: Navigates to Manage Requests
       P-->>A: Shows PENDING request
       A->>P: Clicks Review
       P-->>A: Displays full details
       A->>P: Clicks Reject
       P->>U: Sends rejection email
       P-->>A: Request status: REJECTED

Steps:

1. Navigate to **User Registration > Manage Requests**.
2. Locate the pending request and click **Review** to inspect the details.
3. Click **Reject** to deny the registration.
4. The user receives a rejection email, and the request status changes to ``REJECTED``.
