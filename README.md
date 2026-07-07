Backend web application developed using Django Rest Framework (DRF) to simulate a company desk reservation system. The application enables users to manage office floors, desks, and reservations through a fully RESTful API.

Key features include:
- Multi-floor office structure with desk allocation capabilities.
- Reservation system implementing date-based booking logic.
- Nested and flexible API serializers for diverse data representations.
- Advanced filtering system for availability and reservation queries.
- Role-based access control ensuring secure operations.

The project is supported by comprehensive API documentation, accessible via Swagger UI (/api/docs) and powered by drf-spectacular, facilitating seamless exploration and testing of endpoints.
Responsibilities:
• Designed and implemented the full backend architecture using Django and Django Rest Framework.  
• Developed a relational data model representing floors, desks, and reservations with enforced database constraints.  
• Built a complete RESTful API supporting CRUD operations for all core entities.  
• Implemented multiple serializer strategies (nested, flat, and optimized representations) to support diverse client needs.  
• Created custom validation logic to prevent double booking of desks on the same date.  
• Integrated django-filter to enable advanced query filtering for reservations and desk availability.  
• Implemented role-based permissions, including admin, authenticated users, and read-only access control.  
• Developed a desk availability endpoint with custom filtering logic for real-time resource checking.  
• Integrated drf-spectacular to generate and expose interactive API documentation via Swagger UI.  
• Ensured scalability and maintainability through modular design and separation of concerns across models, serializers, views, and filters.  

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
