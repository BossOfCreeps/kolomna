from collections import defaultdict

from tickets.models import PurchaseEvent
from users.models import CustomUser


def parse_users_by_purchase_events(start_date, end_date, events, no_events):
    qs = PurchaseEvent.objects.all()

    if start_date:
        qs = qs.filter(start_at__date__gte=start_date)

    if end_date:
        qs = qs.filter(end_at__date__lte=end_date)

    users_data = defaultdict(set)
    for obj in qs:
        users_data[obj.purchase.user].add(str(obj.event.id))

    good_events = set(events)
    bad_events = set(no_events)

    result = []
    for user in CustomUser.objects.filter(is_tic_employee=False):
        user_events = users_data.get(user)

        if not (
            (good_events and not user_events)
            or (good_events and user_events and not good_events.issubset(user_events))
            or (bad_events and bad_events.intersection(user_events))
        ):
            result.append(user)

    return result
