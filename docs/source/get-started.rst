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
The Settings page is your central configuration hub. Access it by clicking the **Colfax Connect** menu item in the WordPress admin sidebar. The page is organized into collapsible sections. Each section can be expanded or collapsed by clicking its header.

Project Configuration
"""""""""""""""""""""

These settings define the portal's identity, default access behavior, and security constraints.

**Portal Project Name** -- The display name for your test drive project. Appears in the portal header, admin bar, and all email notifications. Also used to identify the project in API calls to external Colfax services.

**Custom Header Code (HTML)** -- Inject custom CSS or HTML into the ``<head>`` of every portal page. Use this for branding overrides, analytics scripts, or custom styling without modifying theme files.

**One Time Access (OTA)** -- Toggle that controls whether users can make multiple reservations during their access period. When enabled, users may only reserve a seat once before their access concludes. When disabled, users can make repeated reservations until their access end date.

**Default Project Access Period** -- Number of days a user has access after registration approval. Applies to all new registrations unless overridden per user.

**Default Reservation Duration** -- Number of hours allocated for each individual system reservation. Admins can override this per user when processing registration requests.

**Default Allowed Hardware Group** -- Comma-separated list of hardware groups assigned to new users upon approval. If left empty, the user may reserve from any available group.

**Default Reservation HW Group** -- The hardware group pre-selected in the reservation form when a user books a system.

**Blacklist Email Domains** -- Comma-separated list of email domains restricted from registration. Domains are entered without the ``@`` symbol (e.g., ``example.com,spam.org``).

Instant Access Code Defaults
""""""""""""""""""""""""""""

Default parameters for instant access codes. Individual codes can override these at creation time.

**Default Validity Period** -- Number of days an instant access code remains valid from creation. Users must redeem within this window.

**Default Project Access Period** -- Number of days of access granted when a code is redeemed.

**Default Reservation Duration** -- Number of hours allocated per reservation for code-redemption users.

API Configuration
"""""""""""""""""

Credentials and endpoints for connecting to Colfax backend services. All communication uses JWT (HS256) authentication.

**API ISS / API ISS Secret** -- JWT issuer and signing secret for Colfax Connect API authentication.

**Project API ISS / Project API ISS Secret** -- JWT issuer and signing secret for project-specific API calls.

**DB API URL** -- Base URL for the Colfax database API. Used for account provisioning and access management.

**Email Validation API URL** -- External service for email address validation during registration.

**Reservation API URL** -- Base URL for reservation management.

**Infrastructure API URL** -- Base URL for seat status, hardware groups, and infrastructure queries.

**Seat Connected Systems API URL** -- Base URL for connected system management.

**SMTP API URL** -- Base URL for the email delivery service.

REST API Authentication
"""""""""""""""""""""""

JWT credentials for external clients integrating with the portal's REST endpoints. Two tiers are supported:

**JWT Issuer (Colfax Services) / JWT Secret (Colfax Services)** -- For internal Colfax service-to-service authentication.

**JWT Issuer (Client) / JWT Secret (Client)** -- For external client applications.

**JWT Token Validity** -- Maximum age in seconds that a JWT token is accepted from its issuance time.

reCAPTCHA
"""""""""

**Site Key** -- Google reCAPTCHA site key displayed to users on the registration form.

**Secret Key** -- Server-side secret key used to verify user responses.

Email Management
""""""""""""""""

Configure sender identity, subject lines, and HTML body templates for all notification types. Every email template field includes a **Test** button to send a sample email before deploying changes.

**Generic Email Notification** -- Base settings for all outgoing emails:

- **Email Send From** -- Sender email address
- **Email Send From (Name)** -- Sender display name
- **Email Subject** -- Default subject line
- **Email's HTML Body (Project Topic)** -- Project name inserted into email bodies
- **Receiver's Email Address (TEST)** -- Address used for template test sends

**User Registration Emails** -- Templates triggered when a new registration is submitted:

- **Admin's Email Address** -- Receives notification of each new registration
- **New Registration Email Subject** -- Subject line for registration notifications
- **Admin Notification HTML Body** -- Template sent to admin
- **User Confirmation HTML Body** -- Template sent to the registering user

**Project Access Emails** -- Templates for access lifecycle events:

- **Access Approval Email HTML Body** -- Sent when a registration is approved
- **Access Rejection Email HTML Body** -- Sent when a registration is denied
- **Access Deactivation Warning HTML Body** -- Sent before access expires
- **Access Deactivation Email HTML Body** -- Sent when access ends
- **Access Revoke Email HTML Body** -- Sent when admin revokes access
- **Access Expiration Warning Time (Hours)** -- Hours before expiry to send warning. Leave empty to disable.

**Reservation Emails** -- Templates for reservation lifecycle events:

- **Reservation Activation Email HTML Body** -- Sent when a reservation is activated
- **Reservation Deactivation Warning HTML Body** -- Sent before a reservation expires
- **Reservation Deactivation Email HTML Body** -- Sent when a reservation ends
- **Reservation Expiration Warning Time (Hours)** -- Hours before expiry to send warning. Disabled if OTA is enabled.

**User Feedback Emails** -- Templates triggered when a user submits post-session feedback:

- **User Feedback Email HTML Subject** -- Subject line for feedback notifications
- **User Feedback Email HTML Body** -- Template with placeholders for ``[FEEDBACK]``, ``[SEAT]``, ``[RESERVATION_ID]``, ``[USEREMAIL]``, and ``[READY]``

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
