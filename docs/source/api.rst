API
===

The WP Colfax Connect plugin exposes REST API endpoints through the WordPress REST API infrastructure. All endpoints are prefixed with ``/wp-json/`` and fall into two categories:

.. mermaid::

   graph LR
       subgraph External Clients
           A[External App / CRM]
       end
       subgraph WordPress Plugin
           B[JWT Validation]
           D[Client Endpoints<br>external/v1/*]
           E[Service Endpoints<br>cc-template/v1/*,<br>cc-user-registration/v1/*]
       end
       subgraph Colfax Backend
           F[DB API]
           G[Reservation API]
           H[Infrastructure API]
           I[SMTP API]
       end
       A -->|JWT auth| D
       D -->|JWT auth| F
       E -->|Colfax JWT| F
       B --> D
       B --> E

Authentication
--------------

All external API endpoints use JWT Bearer Token Authentication. The client includes an ``Authorization: Bearer <token>`` header. The token is validated against the configured JWT issuer and secret.

JWT tokens use the HS256 algorithm. Two JWT credential pairs are configured in the plugin settings:

* **Colfax Services JWT** -- For internal Colfax service-to-service communication (used by ``cc-template/v1/*`` and ``cc-user-registration/v1/*`` endpoints)
* **Client JWT** -- For external client applications (used by ``external/v1/*`` endpoints)

The JWT token validity window (in seconds) is also configurable and determines how recently a token must have been issued to be accepted.

Standard Response Format
------------------------

External API endpoints return responses in a standardized JSON format:

.. code-block:: json

   {
       "status": 200,
       "error": "",
       "message": "User successfully registered",
       "timestamp": "2024-10-27T19:00:57PDT"
   }

* ``status`` -- HTTP status code (200, 204, 400, 403, 500)
* ``error`` -- Empty string on success; error description on failure
* ``message`` -- Human-readable status message
* ``timestamp`` -- Server timestamp in the configured WordPress timezone

All external API requests are logged to the ``wp_cc_external_api_logs`` table with the endpoint, method, request data, status code, response data, client IP, and timestamp.

External Client Endpoints
-------------------------

These endpoints require JWT Bearer token authentication using the **Client** JWT credentials.

User Registration
^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Endpoint
     - Method
     - Description
   * - ``/external/v1/user-registration``
     - POST
     - Create a user registration from an external system. Accepts JSON body with ``email_address`` (required), ``first_name``, ``last_name``, ``organization_name``, ``country``, ``purpose`` (all required), ``instant_access_code`` (optional), and ``ip_address`` (optional). If an instant access code is provided and valid, the registration is auto-approved. All requests are logged.

User Reservations Composite
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Endpoint
     - Method
     - Description
   * - ``/external/v1/reservation/composite``
     - GET
     - Retrieve all user reservations with composite details including user email, name, seat name, seat alias, start/end times, status, and timezone. Returns 204 with empty data array when no reservations exist.

Colfax Service Endpoints
------------------------

These endpoints require JWT Bearer token authentication using the **Colfax Services** JWT credentials.

Email Template API
^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Endpoint
     - Method
     - Description
   * - ``/cc-template/v1/access/deactivation``
     - GET
     - Get the access deactivation email template. Requires ``email`` query parameter.
   * - ``/cc-template/v1/access/deactivation_warning``
     - GET
     - Get the access deactivation warning email template. Requires ``email`` query parameter.
   * - ``/cc-template/v1/access/revoke``
     - GET
     - Get the access revocation email template. Requires ``email`` query parameter.
   * - ``/cc-template/v1/reservation/activation``
     - GET
     - Get the reservation activation email template. Requires ``email`` query parameter.
   * - ``/cc-template/v1/reservation/deactivation_warning``
     - GET
     - Get the reservation deactivation warning email template. Requires ``email`` query parameter.
   * - ``/cc-template/v1/reservation/deactivation``
     - GET
     - Get the reservation deactivation email template. Requires ``email`` query parameter.

User Registration Lookup
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Endpoint
     - Method
     - Description
   * - ``/cc-user-registration/v1/request``
     - GET
     - Look up a user's email address by their EID. Requires ``EID`` query parameter. Only returns results for registrations with ``COMPLETED`` status.

Error Handling
--------------

All endpoints return standard HTTP status codes:

* **200** -- Success
* **204** -- Success with no content (e.g., no reservations found)
* **400** -- Bad request (missing parameters, invalid data, duplicate registration, blacklisted domain, invalid access code)
* **403** -- Unauthorized (missing or invalid authentication)
* **500** -- Internal server error (database issues, API failures)

Error responses include a descriptive ``message`` field indicating the specific cause of failure. All errors from external API endpoints are logged for audit and troubleshooting purposes.
