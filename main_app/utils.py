# coding: utf-8

from main_app.models import Participant


def attach_info(dict_):
    return dict({
        'num_participants': len(Participant.objects.all()),
        'number_not_null': len([x for x in Participant.objects.all() if x.test_number is not None and x.test_number != '']),
        'participants_with_score': len([x for x in Participant.objects.all() if x.sum is not None and x.sum != '']),
    }, **dict_)
