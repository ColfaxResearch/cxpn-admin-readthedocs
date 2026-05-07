Portal Settings
===============

The Portal Settings page is accessible from the **Colfax Connect** menu in the WordPress admin sidebar. It is organized into collapsible sections, each covering a specific aspect of portal configuration. Click the arrow next to each section header to expand or collapse it.

.. _projectgenericonfigurations:

Project's Generic Configurations
--------------------------------

These settings define the default behavior of the test drive portal for all users.

Portal Project Name
^^^^^^^^^^^^^^^^^^^
The display name for your test drive project. This name appears in the portal header, admin bar, and email notifications. It is also used to identify the project in API calls to external Colfax services.

*Setting key: ``portal_project_name``*

Custom Header Code (HTML)
^^^^^^^^^^^^^^^^^^^^^^^^^
Inject custom CSS or HTML into the ``<head>`` of every portal page. Use this to apply branding overrides, embed analytics scripts, or add custom styling without modifying theme files.

*Setting key: ``custom_header_code``*

One Time Access (OTA)
^^^^^^^^^^^^^^^^^^^^^
A toggle that controls whether users can make multiple reservations during their access period.

* **Enabled** -- Users can only reserve a seat once during their entire project access period. After their reservation ends and feedback is submitted, their access concludes.
* **Disabled** -- Users can make multiple reservations as long as their project access is active and within their access end date.

*Setting key: ``one_time_access``*

Default Project Access Period
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The number of days a user has access to the test drive environment after their registration is approved. This applies to all new registrations unless overridden on a per-user basis. Must be a positive integer.

*Setting key: ``default_access_period`` (value in days)*

Default Reservation Duration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The number of hours allocated for each individual system reservation. When a user books a time slot, this value determines the length of their session. Admins can override this per user when processing registration requests. Must be a positive integer.

*Setting key: ``default_reservation_duration`` (value in hours)*

Default Allowed Hardware Group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Comma-separated list of hardware groups that new users are assigned to upon registration approval. If no hardware group is selected, the user can reserve a system from any available group. The available groups are dynamically fetched from the infrastructure API.

*Setting key: ``default_allowed_hardware_group``*

Default Reservation HW Group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The default hardware group pre-selected in the reservation form when a user books a system. This helps guide users toward the appropriate hardware type for their needs.

*Setting key: ``default_reservation_hw_group``*

Blacklist Email Domains
^^^^^^^^^^^^^^^^^^^^^^^
Comma-separated list of email domains that are restricted from submitting registration requests. Registrations from blacklisted domains are rejected before the request is processed. Domains should be entered without the ``@`` symbol (e.g., ``example.com,spam.org``). Each domain is validated for proper format (valid characters, no consecutive dots, no leading/trailing hyphens, max 253 characters).

*Setting key: ``blacklist_email_domains``*

Instant Access Code Configurations
----------------------------------

These settings define the default parameters for instant access codes. Individual codes can override these defaults at creation time.

Default Validity Period
^^^^^^^^^^^^^^^^^^^^^^^
The number of days an instant access code remains valid from its creation date. Users must redeem the code within this window. Must be a positive integer.

*Setting key: ``default_access_code_validity_period`` (value in days)*

Default Project Access Period
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The number of days of project access granted when a user redeems an instant access code. Must be a positive integer.

*Setting key: ``default_access_code_access_period`` (value in days)*

Default Reservation Duration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The number of hours allocated per reservation for users who accessed via an instant access code. Must be a positive integer.

*Setting key: ``default_access_code_reservation_duration`` (value in hours)*

Colfax Connect API Configurations
----------------------------------

These settings configure the connection to external Colfax backend services. All API communication uses JWT (HS256) authentication.

* **API ISS** -- JWT issuer identifier for Colfax Connect API authentication. (*Setting key: ``colfax_connect_api_iss``*)
* **API ISS Secret** -- JWT signing secret for Colfax Connect API. (*Setting key: ``colfax_connect_api_iss_secret``*)
* **Project API ISS** -- JWT issuer for project-specific API calls. (*Setting key: ``colfax_connect_project_api_iss``*)
* **Project API ISS Secret** -- JWT signing secret for project API. (*Setting key: ``colfax_connect_project_api_iss_secret``*)
* **DB API URL** -- Base URL for the Colfax database API. Used for account provisioning, access management, and user lookup. (*Setting key: ``db_api_url``*)
* **Email Validation API URL** -- External service URL for email address validation during registration. (*Setting key: ``email_validation_api_url``*)
* **Reservation API URL** -- Base URL for the reservation management API. (*Setting key: ``reservation_api_url``*)
* **Infrastructure API URL** -- Base URL for the infrastructure API. Used for seat status, hardware groups, and infrastructure queries. (*Setting key: ``infrastructure_api_url``*)
* **Seat Connected Systems API URL** -- Base URL for the connected systems API. (*Setting key: ``seat_connected_systems_api_url``*)
* **SMTP API URL** -- Base URL for the email delivery service. (*Setting key: ``smtp_api_url``*)

All of the above fields except ``seat_connected_systems_api_url`` are mandatory and must be non-empty to save settings.

Securely Exposed REST APIs
--------------------------

Configure JWT credentials for external clients that need to integrate with the portal's REST API endpoints. Two tiers of JWT authentication are supported:

* **JWT Issuer (Colfax Services)** -- Issuer identifier for internal Colfax service-to-service authentication. (*Setting key: ``exposed_external_api_colfax_iss``*)
* **JWT Secret (Colfax Services)** -- Signing secret for Colfax services. (*Setting key: ``exposed_external_api_colfax_iss_secret``*)
* **JWT Issuer (Client)** -- Issuer identifier for external client applications. (*Setting key: ``exposed_external_api_client_iss``*)
* **JWT Secret (Client)** -- Signing secret for external clients. (*Setting key: ``exposed_external_api_client_iss_secret``*)
* **JWT Token Validity** -- Maximum age (in seconds) that a JWT token is considered valid from its issuance time. Must be a positive integer. (*Setting key: ``exposed_external_api_client_token_validity``*)

Google reCAPTCHA Secrets
------------------------

* **Site Key** -- Your Google reCAPTCHA site key, displayed to users in the registration form. (*Setting key: ``google_recaptcha_site_key``*)
* **Secret Key** -- Your Google reCAPTCHA server-side secret key used to verify user responses. (*Setting key: ``google_recaptcha_secret_key``*)

Both fields are mandatory. reCAPTCHA validation runs on every public registration form submission.

Generic Email Notification Configurations
-----------------------------------------

These settings apply to all email notifications sent by the plugin. When an SMTP API URL is configured, these fields become mandatory:

* **Email Send From** -- The sender email address for all notifications. (*Setting key: ``smtp_email_from``*)
* **Email Send From (Name)** -- The display name shown as the sender. (*Setting key: ``smtp_email_from_name``*)
* **Email Subject** -- Default subject line for notifications. (*Setting key: ``smtp_email_subject``*)
* **Email's HTML Body (Project Topic)** -- Project name text inserted into email body templates. (*Setting key: ``smtp_email_body_project_topic``*)
* **Receiver's Email Address (TEST)** -- Email address used when testing email templates from the settings page. (*Setting key: ``smtp_email_test``*)

User's Registration Notification (Email Templates)
--------------------------------------------------

Configure the emails sent when a new user submits a registration request.

* **Admin's Email Address** -- The admin email that receives notification of each new registration. (*Setting key: ``admin_email``*)
* **New Registration Email Subject** -- Subject line for registration notifications. (*Setting key: ``smtp_newreg_email_subject``*)
* **Admin Notification HTML Body** -- HTML template for the admin notification email. Includes a **Test** button. (*Setting key: ``newreg_email_admin_notification_body``*)
* **User Confirmation HTML Body** -- HTML template for the user's registration confirmation email. Includes a **Test** button. (*Setting key: ``newreg_email_user_notification_body``*)

Templates support placeholder variables that are substituted with user-specific data at send time (e.g., user email, registration ID, project name, dates).

User's Project Access Notification (Email Templates)
----------------------------------------------------

Configure emails related to project access lifecycle events. Each template includes a **Test** button.

* **Access Approval Email HTML Body** -- Sent when a registration is approved. (*Setting key: ``smtp_email_approval_body``*)
* **Access Rejection Email HTML Body** -- Sent when a registration is rejected. (*Setting key: ``smtp_email_rejection_body``*)
* **Access Deactivation Warning Email HTML Body** -- Sent before access expires. (*Setting key: ``smtp_email_access_deactivation_warning_body``*)
* **Access Deactivation Email HTML Body** -- Sent when access ends. (*Setting key: ``smtp_email_access_deactivation_body``*)
* **Access Revoke Email HTML Body** -- Sent when access is revoked by an admin. (*Setting key: ``smtp_email_revoke_body``*)
* **Access Expiration Warning Before End Time (Hours)** -- Number of hours before access expires to send the warning email. Leave empty to disable this feature. (*Setting key: ``default_access_expiration_warning_time``*)

User's Reservation Notification (Email Templates)
-------------------------------------------------

Configure emails related to reservation lifecycle events. Each template includes a **Test** button.

* **Reservation Activation Email HTML Body** -- Sent when a reservation is activated. (*Setting key: ``smtp_email_reservation_activation_body``*)
* **Reservation Deactivation Warning Email HTML Body** -- Sent before a reservation expires. (*Setting key: ``smtp_email_reservation_deactivation_warning_body``*)
* **Reservation Deactivation Email HTML Body** -- Sent when a reservation ends. (*Setting key: ``smtp_email_reservation_deactivation_body``*)
* **Reservation Expiration Warning Before End Time (Hours)** -- Number of hours before reservation expires to send the warning email. Disabled if One Time Access is enabled. (*Setting key: ``default_reservation_expiration_warning_time``*)

User's Feedback Notification (Email Templates)
----------------------------------------------

Configure the email sent to admins when a user submits post-session feedback.

* **User Feedback Email HTML Subject** -- Subject line for feedback notifications. (*Setting key: ``smtp_user_feedback_subject``*)
* **User Feedback Email HTML Body** -- HTML template for the feedback notification. Supports placeholders: ``[FEEDBACK]``, ``[SEAT]``, ``[RESERVATION_ID]``, ``[USEREMAIL]``, ``[READY]``. Includes a **Test** button. (*Setting key: ``smtp_user_feedback_body``*)
