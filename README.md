DRF project simulating desk reservation system in a company. 
Admin can create Users
Admin can create Floor numbers
Admin can create Desk numbers (Desk - ForeignKey with Floor)
User can create a Reservation of a desk for a given date (Reservation - ForeignKey with Desk)

After running project, API documentation is available at /api/docs/ (drf_spectacular).
