DRF project simulating desk reservation system in a company. 

Admin can:
-create Users 
-create Floor numbers 
-create Desk numbers
-create Reservation of a desk for a given date
-use filters by or combined:
    - floor
    - desk
    - reservation date
    - reservation done by specyfic user
    - search for empty desks

User can create: 
-Reservation of a desk for a given date
-use filters same as admin 

After running project, API documentation is available at /api/docs/ (drf_spectacular).

Admin:
login: admin
pw: *6MHVo8w3ty7

Example user:
login: stevenskim
pw: uF6e&EqMi)

Desks numbers were added by utils/.../generate_desks.py
Users were added by utils/.../generate_users.py
Reservations were added by utils/.../generate_reservations.py