# Cinema website

Roles - simple user, admin

- Login, logout, and registration functionality must be implemented on the site.
- Simple user should be automatically logged out after 1 minute of inactivity on the server.

User actions:

Admin:

- Can create a theater hall, that require the hall's name and size.
- Can create movie sessions, specifying the start time, end time, show dates (from February 5th 
to February 15th, 2021, for example), and ticket price for the session.
- Can modify a hall or session if no tickets have been purchased for that hall or session.
- Sessions in the same hall cannot overlap.

Simple users:

- Can view the list of sessions for today and in a separate tab for tomorrow, the number of 
available seats in the hall, purchase a ticket\tickets for a session, and if the seats 
in the hall are sold out, should receive a corresponding notification.
- Can view the list of purchases made by them and the total amount spent over time.
- Sessions can be sorted by price or start time.
- An unauthenticated user sees the list, can sort it, but cannot make any purchases.
