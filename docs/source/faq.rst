FAQ
===

General
-------

What is the WP Colfax Connect plugin?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
WP Colfax Connect is a WordPress plugin that powers the Colfax Experience Center test drive portal. It manages user registration, access provisioning, system seat reservations, SSH key management, user feedback, and integrates with external Colfax backend services via REST APIs.

What database tables does the plugin create?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The plugin creates six custom tables on activation:

* ``wp_cc_user_registrations`` -- User registration requests and their status
* ``wp_cc_user_registration_meta`` -- Key-value metadata for each registration
* ``wp_cc_account_meta`` -- Key-value metadata per user account
* ``wp_cc_instant_access_codes`` -- Instant access codes for events
* ``wp_cc_user_feedback`` -- Post-session feedback entries
* ``wp_cc_external_api_logs`` -- External API request logs

How does the user lifecycle work?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. User submits a registration request (or uses an instant access code)
2. Admin reviews and approves the request (or auto-approval with instant access code)
3. Plugin provisions the user's project access via the Colfax DB API
4. User reserves a time slot from the available reservation grid
5. Plugin activates the reservation and provisions connected system credentials
6. User accesses the assigned system
7. After the session, user submits feedback
8. The reservation is deleted

One Time Access (OTA)
---------------------

What is One Time Access (OTA)?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
OTA is a setting that restricts users to making only one reservation during their entire project access period. When enabled, after the user's single reservation ends and feedback is submitted, their access concludes -- even if their access end date has not yet passed.

When OTA is disabled, users can make multiple reservations as long as their project access is active.

How does OTA interact with reservation expiration warnings?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When OTA is enabled, the reservation expiration warning feature is automatically disabled, since the user only has one reservation and the warning is not applicable.

Instant Access Codes
--------------------

How do I create an instant access code?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Navigate to **User Registration > Instant Access Codes** in the admin panel, click **Add New**, and fill in the code details including event name, validity period, access period, reservation duration, hardware group, max users, one-time access toggle, whitelisted email domains, and description.

Why is my instant access code showing as invalid?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
An instant access code may be invalid for several reasons:

* The current date is outside the code's validity window (before ``validity_start_date`` or after ``validity_end_date``)
* The code has reached its maximum usage count (``usage_count`` >= ``max_users``)
* The user's email domain is not in the code's whitelisted domains (if whitelisting is configured)
* The code was deleted or its status was changed

Registration and Access
-----------------------

Why can't a user submit another registration request?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The plugin prevents duplicate registrations. If a user already has a registration with ``PENDING`` or ``APPROVED`` status, any new submission from the same email address will be rejected. The existing request must be processed (approved, rejected, or completed) before a new one can be submitted.

How do I extend a user's access period?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Navigate to **Project Management > Project Access**, find the user, click **Edit**, modify the **End Date**, and click **Update**. This override takes precedence over the default access period.

How do I change a user's reservation duration?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the quick edit feature in either **Manage Requests** or **Project Access**. Modify the **Reservation Duration** field and save. The new duration applies to the user's future reservations.

Why was a user's registration rejected?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Common reasons include:

* The email domain is in the blacklist
* The email address failed external validation
* reCAPTCHA verification failed
* Required form fields were missing or invalid
* A duplicate registration already exists

Server and Reservation Management
---------------------------------

What do the seat status codes mean?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **0 (Admin Only)** -- Available only for manual admin assignment
* **1 (Maintenance)** -- Unavailable for all reservations
* **2 (Public)** -- Available in the public reservation pool

How do I manually assign a reservation to a user?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Navigate to **Project Management > Reservations**, click **Add Reservation**, select the user, choose a seat, set the time range, and click **Create**.

How do I export reservation data?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the **Reservations** table, use the **Export** action to download all reservations as CSV or Excel files. This is useful for analytics and reporting.

Email Notifications
-------------------

How do I test an email template?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Each email template field in the settings page has a **Test** button next to it. Click the button to send a sample email to the test email address configured in **Generic Email Notification Configurations**.

How do email template placeholders work?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Email templates support placeholder variables that are replaced with actual values at send time. Common placeholders include:

* ``[USEREMAIL]`` -- User's email address
* ``[PROJECTNAME]`` -- Portal project name
* ``[ACCESS_START_TIME]`` -- Access start date/time
* ``[ACCESS_END_TIME]`` -- Access end date/time
* ``[FEEDBACK]`` -- User's feedback text
* ``[SEAT]`` -- Seat name
* ``[RESERVATION_ID]`` -- Reservation identifier
* ``[READY]`` -- User's ready/not-ready response

API Integration
---------------

How do I authenticate API requests?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Internal endpoints use the ``X-User`` header with the user's EID. External endpoints use JWT Bearer tokens in the ``Authorization`` header. JWT credentials are configured in the **Securely Exposed REST APIs** settings section.

Where can I view API request logs?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Navigate to the **External API Logs** table under the External APIs section. All external API requests are logged with full request/response details, status codes, timestamps, and client IP addresses.

Why am I getting a 403 error on an external API endpoint?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A 403 error typically means:

* The ``Authorization`` header is missing
* The JWT token has expired (beyond the configured validity window)
* The JWT token was signed with an incorrect secret or issuer
* The token's issuer (ISS) doesn't match the configured credentials
