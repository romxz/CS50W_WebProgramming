from flights.models import Flight

f = Flight(origin="New York", destination="London", duration=415)
f.save()

Flight.objects.all()
# If no __str__ method on Flight:
# Returns <QuerySet [<Flight: Flight object(1)>]>
# If __str__ method on Flight, e.g.:
# Returns <QuerySet [<Flight: 1 - New York to London>]>

f = Flight.objects.first()

f
# Returns <Flight: 1 - New York to London>

f.origin()
# Returns 'New York'

f.id
# Returns 1

f.delete()
# Deletes the flight as expected
