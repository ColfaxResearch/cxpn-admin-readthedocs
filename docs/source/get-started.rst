..
    Use this document to describe the overall flow of how to add users, manage reservations, provisioning, etc.

Get Started
===========

Once you have gained access to the portal, you will be presented with the following menu elements.

.. image:: /images/nav.png
  :alt: Test drive portal menu items.

Each section is organized to help you efficiently navigate and manage different aspects of our test drive program. The **Plugin** section allows you to configure settings specific to the portal, including but not limited to test drive duration, API configurations, and email templates sent to users.

The **User Registration** section provides tools for managing incoming user requests from registration forms, manually inviting users, and managing access codes for events and training sessions.

**Project Management** helps you oversee who has access to the test drive, along with any active reservations.

The **Infrastructure** section allows you to monitor your server assets along with their status.

**External APIs** provide documentation and logs for integration and troubleshooting.

The sections below contain a detailed breakdown of each menu category and its key functions.

Plugin
------

Settings
^^^^^^^^
The Settings page is your central configuration hub. Access it by clicking the **Colfax Connect** menu item in the WordPress admin sidebar. This page is organized into collapsible sections covering all aspects of portal behavior:

* **Project's Generic Configurations** -- Portal name, default access periods, reservation durations, hardware group assignments, and email domain blacklisting
* **Instant Access Code Configurations** -- Default validity periods and access parameters for event-based instant access codes
* **Colfax Connect API Configurations** -- JWT credentials and API URLs for connecting to Colfax backend services (database, reservation, infrastructure, SMTP, etc.)
* **Securely Exposed REST APIs** -- JWT credentials for external client integration
* **Google reCAPTCHA Secrets** -- Site and secret keys for bot protection on registration forms
* **Email Notification Configurations** -- Sender address, subject lines, and HTML body templates for all notification types
* **User Registration Emails** -- Admin notification and user confirmation templates
* **Project Access Emails** -- Approval, rejection, deactivation warning, deactivation, and revocation templates
* **Reservation Emails** -- Activation, deactivation warning, and deactivation templates
* **User Feedback Emails** -- Subject and body templates for post-session feedback notifications

Each email template includes a **Test** button that sends a sample email so you can verify formatting and placeholder substitution before deploying changes.

User Registration
-----------------

Manage Requests
^^^^^^^^^^^^^^^
The **Manage Requests** table displays all user registration submissions. Each row shows the user's email, registration date, access period, reservation duration, hardware group assignment, and current request status.

Request statuses include:

* **PENDING** -- Awaiting admin review
* **APPROVED** -- Admin has approved; user can now reserve a system
* **COMPLETED** -- User has used their access and the period has ended
* **REJECTED** -- Admin has denied the request
* **REVOKE** -- Admin has revoked previously granted access

Available actions per request:

* **Approve** -- Approves the registration and provisions project access via the external Colfax DB API. An approval email is sent to the user.
* **Reject** -- Denies the registration. A rejection email is sent to the user.
* **Review** -- Opens the registration details for inspection, including all submitted form metadata fields.
* **Quick Edit** -- Allows inline modification of the end date, reservation duration, and hardware group assignment without leaving the table.
* **Delete** -- Removes the registration request entirely.

The table supports global search across all columns and status-based filtering for efficient management.

Instant Access Codes
^^^^^^^^^^^^^^^^^^^^
Instant Access Codes provide a way to grant immediate project access to users without manual admin review -- useful for events, training sessions, and demo days.

To create an instant access code:

1. Navigate to the **Instant Access Codes** tab under User Registration.
2. Click **Add New** and fill in the code details:
   - **Event Name** -- Label for the event or session
   - **Project Name** -- Associated project
   - **Validity Period** -- Date range during which the code can be used
   - **Access Period** -- Number of days of access granted upon use
   - **Reservation Duration** -- Hours allocated per reservation
   - **Hardware Group** -- Which hardware group(s) the user can reserve
   - **Max Users** -- Maximum number of redemptions allowed
   - **One-Time Access** -- Whether the user can only reserve once
   - **Whitelist Email Domains** -- Restrict usage to specific email domains
   - **Description** -- Notes about the code's purpose

When a user enters a valid instant access code on the registration form, their request is automatically set to **APPROVED** status, and access is provisioned immediately. The code's ``usage_count`` increments with each redemption.

Project Management
------------------

Project Access
^^^^^^^^^^^^^^
The **Project Access** table shows all users who have been granted access to the test drive environment. Each entry displays:

* User email address
* Access start and end dates
* Reservation duration (hours)
* Assigned hardware group(s)
* One-time access setting
* Current access status

Available actions:

* **Quick Edit** -- Override the end date, modify reservation duration, or change hardware group assignment for a specific user
* **End Access** -- Immediately terminate a user's project access
* **Review** -- View full access details and provisioning information

When a user's registration is approved, the plugin calls the external Colfax DB API to provision their account authorization. The access record includes start/end timestamps, hardware group permissions, and reservation parameters.

Reservations
^^^^^^^^^^^^
The **Reservations** table provides a comprehensive view of all user reservations across the infrastructure. Each reservation records:

* User email and name
* Reservation ID
* Seat (system) name and alias
* Hardware group
* Start and end times
* Reservation status (activated, pending, etc.)

Available actions:

* **Add Reservation** -- Manually create a reservation for a specific user and time slot
* **Edit** -- Modify an existing reservation's time slot or seat assignment
* **Delete** -- Remove a reservation
* **Reprovision** -- Re-provision a reservation through the external reservation API
* **Reassign** -- Move a reservation to a different seat
* **Export** -- Download all reservations as CSV or Excel via the ``export_all_reservations`` handler

The table supports global search, status filtering, and column sorting.

Infrastructure
--------------

Servers/Seats
^^^^^^^^^^^^^
The **Servers/Seats** table lists all compute systems in the infrastructure. Each seat entry shows:

* Seat ID and name
* Alias name (human-readable label shown to users)
* Current status
* Connected systems and their details

Seat status codes:

* **0 (Admin Only)** -- Not available in the public reservation pool. Only admins can manually assign reservations.
* **1 (Maintenance)** -- Unavailable for both public and manual reservations.
* **2 (Public)** -- Available in the public reservation pool and for manual reservation assignment.

Available actions:

* **Edit Alias** -- Update the human-readable name displayed to users
* **Update Status** -- Change the seat's availability status
* **Connected Systems** -- Manage connected systems (add, edit, delete)
* **Apply DHCP** -- Apply DHCP configuration to a seat's connected system
* **Bulk Add** -- Add multiple connected systems at once

External APIs
-------------

Documentation
^^^^^^^^^^^^^
The **API Documentation** page provides auto-generated Swagger UI documentation for all externally exposed REST endpoints. This includes:

* Client-facing APIs for user registration and reservation data
* Colfax service APIs for email template retrieval
* Authentication requirements (JWT Bearer tokens)
* Request/response schemas with example payloads

The documentation is accessible from the admin panel and updates automatically as new endpoints are added or modified.

Logs
^^^^
The **External API Logs** table maintains a record of all API activity for monitoring and troubleshooting. Each log entry captures:

* API endpoint and HTTP method
* Request data (payload)
* Response status code
* Response data
* Client IP address
* Timestamp

Use the logs to diagnose integration issues, audit API usage, and verify that external services are communicating correctly with the portal. The table supports filtering by endpoint, status code, and date range.
