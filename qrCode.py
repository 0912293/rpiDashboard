import qrcode


def generateBookingQr(filename, date, selected, slots ,room):
    print(filename + 'qr/qr.png')
    print(date.day())
    print(date.month())
    print(date.year())
    print(slots)
    print(selected)
    print(int(selected) + int(slots - 1))
    pix = qrcode.make(
        '{"reservation": {"timeslotfrom": %s, "timeslotto": %s, "date": "%s-%s-%s", "room": "%s"}}' % (
            selected,
        int(selected) + int(slots - 1),
        date.day(), date.month(), date.year(), room))
    pix.save(filename)
    print("qr generated")


def generateDefectQr(filename, type, room):
    pix2 = qrcode.make(
        '{"defunct": {"type": "%s", "room": "%s"}}' % (type, room))
    pix2.save(filename)
    print("qr generated")
