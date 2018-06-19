import qrcode


def generate_booking_qr(filename, date, selected, slots, room):
    pix = qrcode.make(
        '{"reservation": {"timeslotfrom": %s, "timeslotto": %s, "date": "%s-%s-%s", "room": "%s"}}' %
        (selected, int(selected) + int(slots - 1), date.day(), date.month(), date.year(), room))
    pix.save(filename)


def generate_defect_qr(filename, type, room):
    pix2 = qrcode.make(
        '{"defunct": {"type": "%s", "room": "%s"}}' % (type, room))
    pix2.save(filename)
