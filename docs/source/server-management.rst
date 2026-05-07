Server Management
=================

The following diagram shows the infrastructure management workflow:

.. mermaid::

   graph TB
       A[Infrastructure Seat] --> B{Seat Status}
       B -->|0 - Admin Only| C[Available for manual<br>admin assignment only]
       B -->|1 - Maintenance| D[Unavailable for all<br>reservations]
       B -->|2 - Public| E[Available in public<br>reservation pool]
       C --> F[Admin manually<br>assigns reservation]
       E --> G[User self-service<br>reservation]
       F --> H[Connected systems<br>provisioned]
       G --> H
       H --> I[DHCP applied<br>if configured]
       I --> J[User receives credentials<br>and SSH config]

.. _setcomputealias:

Set Compute Alias
-----------------

The compute alias is a human-readable label displayed to users in the reservation interface instead of the internal seat identifier. Setting meaningful aliases helps users identify the type of system they're reserving.

To set or update a compute alias:

1. Navigate to **Infrastructure > Servers/Seats** in the admin panel.
2. Locate the seat in the table.
3. Click **Edit Alias** in the action column.
4. Enter the desired alias name (e.g., ``GPU-Server-01``, ``CPU-Cluster-A``, ``Edge-Device-3``).
5. Click **Save** to apply the change.

The alias is stored in the infrastructure database and is reflected immediately in the user-facing reservation form and connected systems table.

.. _setcomputestatus:

Set Compute Status
------------------

System status is an attribute that defines how a compute resource is presented to the portal and whether it's available for reservation.

Status codes:

- **0 (Admin Only)** -- System is not available in the public reservation pool. Only administrators can manually assign reservations to this seat. Use this status when:

  - Reserving a system for a VIP or priority user
  - Testing new hardware before making it publicly available
  - Dedicating a system for internal development or QA work
  - A system has limited capacity and should only be assigned by request

- **1 (Maintenance)** -- System is unavailable for both public and manual reservations. Use this status when:

  - Performing hardware upgrades or repairs
  - Running firmware updates
  - Investigating system issues
  - Taking a system offline for extended periods

- **2 (Public)** -- System is available in the public reservation pool and for manual reservation assignment. This is the default status for healthy, operational systems.

To change a seat's status:

1. Navigate to **Infrastructure > Servers/Seats**.
2. Locate the seat and click **Edit** in the action column.
3. Select the desired status from the dropdown (0, 1, or 2).
4. Click **Update** to save.

When a seat's status changes from **Maintenance** (1) back to **Public** (2) or **Admin Only** (0), it becomes available for reservation again. The change is reflected in real time in the reservation grid shown to users.

Manually Start Reservation for a User
-------------------------------------

To manually start a reservation for a user on a specific seat:

1. Navigate to **Project Management > Reservations**.
2. Click **Add Reservation**.
3. Select the user by email address.
4. Choose the target seat from the available seats list. Only seats with status **0** (Admin Only) or **2** (Public) will appear.
5. Set the start time and end time for the reservation.
6. Select the hardware group.
7. Click **Create** to provision the reservation.

The plugin calls the external reservation API to create the reservation record. Once activated:

* The user receives a reservation activation email
* The seat's connected systems are provisioned with credentials
* The user can view their reservation details, connected system information, and SSH port forwarding configuration from the portal

To reassign an existing reservation to a different seat:

1. In the Reservations table, locate the reservation.
2. Click **Reassign** in the action column.
3. Select the new target seat.
4. Confirm the reassignment.

The old reservation is deleted and a new one is created on the target seat, with fresh connected system credentials generated for the user.
