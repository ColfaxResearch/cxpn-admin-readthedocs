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
All external API endpoints use JWT Bearer tokens in the ``Authorization`` header. JWT credentials are configured in the **Securely Exposed REST APIs** settings section.

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

Settings & Configuration
------------------------

Why won't my settings save?
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The settings page validates all fields before saving. Common reasons for save failures include:

- A mandatory field is empty (portal project name, default access period, reservation duration, DB API URL, SMTP API URL, etc.)
- A numeric field contains a non-integer or negative value (access period, reservation duration, validity periods)
- A blacklisted email domain has invalid formatting (consecutive dots, leading/trailing hyphens, over 253 characters)
- A default allowed hardware group value doesn't match an active group from the infrastructure API

Validation errors appear at the top of the settings page. Fix the flagged fields and try saving again.

What makes a setting mandatory?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following fields are required and cannot be empty: portal project name, default access period, default reservation duration, default reservation HW group, default access code validity period, default access code access period, default access code reservation duration, DB API URL, email validation API URL, both JWT ISS/Secret pairs, reservation API URL, infrastructure API URL, SMTP API URL, and both reCAPTCHA keys. When an SMTP API URL is configured, the generic email notification fields (sender, name, subject, body topic, test address) also become mandatory.

Can I change settings mid-cycle?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes. Most settings take effect immediately for new operations. However:

- Changing the default access period or reservation duration does not retroactively affect users already in the system. You must manually override those users via Quick Edit.
- Changing API credentials or URLs will affect all subsequent API calls. If the new credentials are invalid, API-dependent features will fail until corrected.
- Changing OTA from enabled to disabled (or vice versa) affects only new reservations going forward.

What happens if I leave a non-mandatory field empty?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Each field has a defined default behavior when left empty:

- **Custom Header Code** -- No custom CSS/HTML is injected
- **Default Allowed Hardware Group** -- If no group is selected, users may reserve from any available group
- **Blacklist Email Domains** -- No domains are restricted
- **Access/Reservation Expiration Warning Time** -- The warning email feature is disabled
- **Seat Connected Systems API URL** -- Connected system features remain inactive

Hardware Groups
---------------

What are hardware groups?
~~~~~~~~~~~~~~~~~~~~~~~~~
Hardware groups are logical categories of compute systems in your infrastructure (e.g., GPU servers, CPU clusters, edge devices). They are defined in the external Colfax infrastructure system and fetched dynamically by the plugin. Hardware groups allow you to segment which types of systems different users can reserve.

How are hardware groups assigned?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When a user's registration is approved, they are assigned the hardware groups specified in the **Default Allowed Hardware Group** setting. You can override this per user by using Quick Edit on their registration request or project access entry. If no group is assigned, the user may reserve from any available group.

Can a user switch hardware groups?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes. Use Quick Edit on the user's entry in either **Manage Requests** or **Project Access** to modify their assigned hardware group. The change takes effect immediately for their next reservation.

SSH Key Management
------------------

How do users add SSH keys?
~~~~~~~~~~~~~~~~~~~~~~~~~~
Users manage their own SSH keys through the portal's SSH Keys page, powered by the ``[cc-list-of-ssh-keys]`` shortcode. The page displays an accordion-style interface where users can upload new keys and delete existing ones. Keys are stored and managed through the external Colfax DB API.

Shortcodes
----------

What are shortcodes?
~~~~~~~~~~~~~~~~~~~~
Shortcodes are WordPress placeholders that render dynamic content on portal pages. They are enclosed in square brackets (e.g., ``[cc-registration-form]``) and are processed by the plugin when the page loads.

Where do I place shortcodes?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Shortcodes can be placed in any WordPress page, post, or widget area. To add a shortcode:

1. Navigate to **Pages** (available to full WordPress admins) and edit the desired page.
2. Insert the shortcode into the page content at the location where you want the content to appear.
3. Save the page.

Available shortcodes include:

* ``[cc-registration-form]`` -- Renders the public user registration form
* ``[cc-reservation-form]`` -- Renders the reservation booking form with available time slots
* ``[cc-list-of-ssh-keys]`` -- Renders the SSH key management interface
* ``[cc-seat-connected-systems-table]`` -- Renders a table of connected systems for the user's active reservation
* ``[cc-ssh-port-forwarding]`` -- Generates SSH config entries for all connected systems
* ``[cc-landing-host-ip]`` -- Displays the landing host IP for the user's active reservation
* ``[cc-if-active-reservation]`` -- Conditionally shows content only if the user has an active reservation
* ``[cc-inject-feedback-form]`` -- Renders the post-session feedback form
* ``[cc-display-feedback]`` -- Displays the user's previous feedback entries
* ``[cc-user-email]`` -- Outputs the current user's email address
* ``[cc-display-if-registration]`` -- Conditionally shows content if the user has a pending registration
* ``[cc-display-if-access]`` -- Conditionally shows content if the user has active project access

Reservation Troubleshooting
---------------------------

Why is the reservation grid empty?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The reservation grid may appear empty for several reasons:

- All seats are set to **Maintenance** (status 1), making none available for public reservation
- The user's assigned hardware group has no active seats
- The user has no active project access or their access has expired
- There are no available time slots within the configured look-ahead window
- The external reservation API is unreachable

Check the **Servers/Seats** table to verify seat statuses and the **Project Access** table to verify the user's access is active.

Why can't a user reserve right now?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Common reasons include:

- The user already has an active reservation and OTA is enabled
- The user's project access has expired or hasn't started yet
- The selected time slot exceeds the user's access end date (unless OTA auto-extends access)
- All seats in the user's allowed hardware group are unavailable
- The reservation slot data has expired (slot data is valid for only 5 minutes; the user must refresh the page)

What happens if two users try to reserve the same time slot?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The reservation system validates availability at the time of booking through the external reservation API. If a slot is already taken, the second user will receive an error. The user should refresh the page to see updated availability.

How do I verify a manually-created reservation was successful?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
After creating a manual reservation, check the **Reservations** table. A successful reservation will appear with status ``activated``. The user should also receive a reservation activation email. If the reservation does not appear, check the **External API Logs** for any failed API calls.

Email Troubleshooting
---------------------

Why aren't emails being sent?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Email delivery failures can be caused by:

- The SMTP API URL is not configured or is unreachable
- The SMTP API credentials are invalid
- The recipient email address is malformed
- The email template is empty

Check the SMTP API URL in **Colfax Connect API Configurations** and verify connectivity to the endpoint. Use the **Test** button on any email template to verify delivery.

Can I customize the sender name and address?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes. Set the **Email Send From** and **Email Send From (Name)** fields in **Generic Email Notification Configurations**. These values are used as the sender for all outgoing emails.

What happens if the SMTP API is down?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If the SMTP API is unreachable, the plugin will log an error but will not interrupt the user flow. Registrations, approvals, and reservations will still be processed -- the user simply won't receive email notifications until the SMTP API is restored.

Timezone & Scheduling
---------------------

What timezone are reservation times shown in?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Reservation times are displayed in the WordPress site's configured timezone (set in **WordPress Settings > General > Timezone**). All internal timestamps are stored as UTC epochs and converted to the site timezone for display.

Can I change the portal timezone?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes. Change the timezone in **WordPress Settings > General**. All reservation times, access dates, and email timestamps will reflect the new timezone going forward. Existing timestamps in the database remain unchanged and are re-rendered in the new timezone.

Admin Role
----------

What is the ``project_dashboard_admin`` role?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``project_dashboard_admin`` is a custom WordPress role created by the plugin on activation. It has the same capabilities as a standard WordPress administrator but receives a streamlined admin interface:

- Default WordPress menus (Posts, Media, Comments, Themes, Plugins, Users, Tools, Settings) are hidden
- The admin sidebar is collapsed, showing only the **Colfax Connect** menu
- The admin bar is hidden
- The admin is redirected to the **Manage Requests** page upon login

This role is intended for portal operators who only need to manage the test drive portal and do not need access to general WordPress administration.

How does it differ from a normal WordPress admin?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A standard WordPress administrator sees the full WordPress dashboard with all menus and settings. The ``project_dashboard_admin`` role sees only the Colfax Connect plugin interface. Both roles have the same underlying capabilities -- the difference is purely in the UI presentation. If you need to access WordPress settings while logged in as ``project_dashboard_admin``, log in with a standard administrator account instead.

reCAPTCHA
---------

Why is reCAPTCHA failing?
~~~~~~~~~~~~~~~~~~~~~~~~~~
reCAPTCHA verification failures occur when:

- The Site Key or Secret Key is not configured in the settings
- The keys are mismatched (the Site Key and Secret Key must belong to the same reCAPTCHA site registration)
- The registered domain for the reCAPTCHA keys doesn't match the portal's domain
- Google's reCAPTCHA service is temporarily unavailable

Verify your keys in **Google reCAPTCHA Secrets** and ensure the domain is registered in your Google reCAPTCHA console.

Can I disable reCAPTCHA?
~~~~~~~~~~~~~~~~~~~~~~~~
reCAPTCHA is mandatory for public registration endpoints. Leaving the Site Key or Secret Key empty will cause settings validation to fail. It is not possible to disable bot protection through the admin interface.

Changelog
---------

Where can I see plugin update history?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The plugin includes a built-in changelog viewer accessible from the admin panel. It renders the ``CHANGELOG.md`` file as formatted HTML and supports downloading the changelog as a PDF. Navigate to the changelog section from the Colfax Connect admin menu.

Operations / Day-to-Day
-----------------------

What's the difference between **Reject** and **Revoke**?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **Reject** is used during the initial review stage. It denies a ``PENDING`` registration request and sends a rejection email. The user's request status changes to ``REJECTED``.
- **Revoke** is used after access has already been granted. It terminates an active or approved user's access and sends a revocation email. The user's request status changes to ``REVOKE``.

Reject prevents access from being granted. Revoke removes access that was already granted.

What happens when a user's access expires but they still have an active reservation?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When a user's project access end date passes, their access is deactivated through the Colfax DB API. Any active reservations associated with that access are invalidated. The user will no longer be able to access the system or make new reservations.

Can I see who redeemed a specific instant access code?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the **Manage Requests** table, filter by the access code or search by the code value. All registrations created through an instant access code have the code recorded in the ``access_code`` field. You can also view the code's ``usage_count`` in the **Instant Access Codes** table to see how many times it has been redeemed.

How do I find all users from a specific organization or country?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the global search in the **Manage Requests** table. The search spans all columns, including metadata fields like organization name and country. For more granular filtering, use the **Review** action on individual entries to inspect their full metadata.

What does the **Review** button show that the table doesn't?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The **Review** action opens the full registration details, including:

- All submitted form metadata fields (first name, last name, organization, country, purpose, IP address, etc.)
- The exact timestamps for registration, access start, and access end
- The user's assigned hardware group and one-time access setting
- Any error responses from previous processing attempts

What happens to a user's data when I delete their registration?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Deleting a registration removes the entry from the ``wp_cc_user_registrations`` table and its associated metadata from ``wp_cc_user_registration_meta``. No notification email is sent. If the user already has active project access, that access is not automatically terminated -- you must manually end their access through **Project Access**.

Troubleshooting
---------------

How do I handle a user who says they never received their approval email?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
First, verify the email was sent by checking the **External API Logs** for a successful SMTP API call. If the email was sent, ask the user to check their spam/junk folder and verify the email address on file by using **Review** on their registration entry.
