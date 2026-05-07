Access Management
=================

The following diagram illustrates the user lifecycle from registration through system access:

.. mermaid::

   graph LR
       A[User submits<br>registration] --> B{Has instant<br>access code?}
       B -->|Yes| C[Auto-approve<br>and provision]
       B -->|No| D[Status: PENDING]
       D --> E{Admin review}
       E -->|Approve| F[Provision access<br>via Colfax DB API]
       E -->|Reject| G[Send rejection<br>email]
       F --> H[Send approval<br>email to user]
       H --> I[User reserves<br>time slot]
       I --> J[Reservation<br>activated]
       J --> K[User accesses<br>assigned system]
       K --> L[Post-session<br>feedback]
       L --> M[Reservation<br>deleted]

.. _inviteusers:

Invite Users
------------

There are three ways to grant users access to the test drive portal:

1. **Registration Form** -- Users submit a registration request through the public-facing form. The request enters ``PENDING`` status and awaits admin review. Upon approval, the plugin provisions the user's project access via the external Colfax DB API and sends an approval email.

2. **Instant Access Codes** -- Admins generate time-limited access codes for events or training sessions. When a user enters a valid code on the registration form, their request is automatically approved without admin intervention. The code validates the email domain against a whitelist, checks the validity window, and verifies the usage count hasn't exceeded the maximum.

3. **External API Registration** -- External systems can submit user registration requests programmatically via the ``POST /wp-json/external/v1/user-registration`` endpoint. This supports bulk onboarding and integration with external CRM or event management systems. The API accepts the same fields as the web form plus an optional instant access code.

When processing a registration request, the plugin performs the following validation chain:

* Google reCAPTCHA verification (web form only)
* Form field presence and required field checks
* XSS sanitization of all input
* Duplicate registration check (prevents multiple PENDING or APPROVED requests from the same email)
* Email address validation via external API
* Blacklisted email domain check

Upon successful validation, the registration is inserted into the ``wp_cc_user_registrations`` table, metadata fields are stored in ``wp_cc_user_registration_meta``, and confirmation emails are sent to both the user and the admin.

.. _removeusers:

Remove Users
------------

To remove a user's access to the test drive:

1. Navigate to **Project Management > Project Access** in the admin panel.
2. Locate the user in the Project Access table.
3. Click **End Access** to immediately terminate their access.

Ending access performs the following actions:

* The user's project access status is updated via the external Colfax DB API
* A deactivation or revocation email is sent to the user (depending on the reason)
* Any active reservations associated with the user's access are invalidated

To remove a pending registration request:

1. Navigate to **User Registration > Manage Requests**.
2. Locate the user's registration entry.
3. Click **Reject** to deny the request (sends a rejection email), or **Delete** to remove the entry entirely without notification.

Set Non-default User Project Access Duration
--------------------------------------------

Use this workflow when a user needs a project access period that differs from the project default.

1. Open the Admin portal and navigate to the Colfax Connect plugin using the left sidebar. In the main pane, navigate to the **Project Access** tab in the **Project Management** section.
2. Find the user whose access end date you would like to override and click **Edit**.
3. In the quick edit menu, select the appropriate **End Date** and time.
4. Save the changes by clicking **Update**.

Notes:

- The user-project override takes precedence over the project default duration.
- The end date cannot be set earlier than the current date if the user has an active reservation extending beyond it.

Set Non-default User Server Reservation Duration
------------------------------------------------

Use this workflow when a user needs a reservation duration that differs from the default.

1. Navigate to **User Registration > Manage Requests** or **Project Management > Project Access**.
2. Find the user and click **Edit** (quick edit).
3. In the quick edit menu, modify the **Reservation Duration** field to the desired number of hours.
4. Click **Update** to save.

Notes:

- The reservation duration defines how long a user can hold a system seat in a single booking.
- This override applies to all future reservations made by the user until changed again.
- If One Time Access (OTA) is enabled globally, the user can only make one reservation regardless of duration.

Manually Start Reservation for a User
-------------------------------------

Use this workflow when you need to manually assign a reservation to a user outside of the self-service reservation form -- for example, to prioritize a user or assign a specific system.

1. Navigate to **Project Management > Reservations** in the admin panel.
2. Click **Add Reservation**.
3. Fill in the reservation details:
   - **User Email** -- The email address of the user to assign the reservation to
   - **Start Time** -- When the reservation becomes active
   - **End Time** -- When the reservation expires
   - **Hardware Group** -- The hardware group the reservation should target
   - **Seat** -- (Optional) A specific seat to assign; if left blank, the system auto-assigns an available seat
4. Click **Create** to provision the reservation via the external reservation API.

The reservation is created in the Colfax reservation system and appears in the Reservations table with status ``activated``. The user receives a reservation activation email with their access details, including the seat name, connected system credentials, and SSH port forwarding commands.
