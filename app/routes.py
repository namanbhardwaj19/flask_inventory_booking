from flask import Blueprint, request, jsonify
from .models import db, Member, Inventory, Booking
from datetime import datetime
import csv
from io import StringIO

bp = Blueprint('main', __name__)


@bp.route('/book', methods=['POST'])
def book_item():
    data = request.get_json()
    member = Member.query.get(data['member_id'])
    inventory = Inventory.query.get(data['inventory_id'])

    if not member or not inventory:
        return jsonify({'error': 'Invalid member or inventory ID'}), 400

    if not member.can_book():
        return jsonify({'error': 'Member has reached max bookings'}), 400
    if inventory.remaining_count == 0:
        return jsonify({'error': 'Item out of stock'}), 400

    booking = Booking(member_id=member.id, inventory_id=inventory.id)
    db.session.add(booking)
    member.booking_count += 1
    inventory.remaining_count -= 1
    db.session.commit()
    return jsonify({'success': 'Booking confirmed'})


@bp.route('/cancel', methods=['POST'])
def cancel_booking():
    data = request.get_json()
    booking = Booking.query.get(data['booking_id'])

    if not booking:
        return jsonify({'error': 'Invalid booking ID'}), 400

    member = Member.query.get(booking.member_id)
    inventory = Inventory.query.get(booking.inventory_id)

    member.booking_count -= 1
    inventory.remaining_count += 1
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'success': 'Booking cancelled'})


@bp.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    stream = StringIO(file.stream.read().decode("utf-8"))
    reader = csv.reader(stream)
    header = next(reader, None)

    if 'members' in file.filename.lower():
        for row in reader:
            db.session.add(Member(first_name=row[0], last_name=row[1], booking_count=int(row[2]),
                                  date_joined=datetime.strptime(row[3], "%Y-%m-%dT%H:%M:%S")))
    elif 'inventory' in file.filename.lower():
        for row in reader:
            db.session.add(
                Inventory(title=row[0], description=row[1],
                          remaining_count=int(row[2]) if row[2].isdigit() else 0,
                          expiration_date=datetime.strptime(row[3], "%d-%m-%Y").date() if row[3] else None))

    db.session.commit()
    return jsonify({'success': 'Data uploaded successfully'})
