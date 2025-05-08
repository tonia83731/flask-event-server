from datetime import datetime, timedelta
from marshmallow import Schema, fields, validate, ValidationError, validates_schema

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
today_timestamp = int(today.timestamp())

def event_date_validation(value):
    three_hrs = datetime.now() + timedelta(hours=3)
    three_hrs_timestamp = int(three_hrs.timestamp())
    if value < three_hrs_timestamp:
        raise ValidationError("Event date must be at least 3 hours from now.")

def apply_date_validation(value):
    if value < today_timestamp:
        raise ValidationError("Apply date cannot be before today.")

# EVENT SETTINGS
class EventValidationForm(Schema):
    """
        title, description, category_id, img_id
        event_start_date, event_end_date
        apply_start_date, apply_end_date
        location, address, url
        max_attendees
    """

    title = fields.String(required=True, validate=validate.Length(min=3, max=255))
    description = fields.String(required=True, validate=validate.Length(max=300))
    category_id = fields.Integer()
    img_id  = fields.Integer()

    event_start_date = fields.Integer(required=True, validate=event_date_validation)
    event_end_date = fields.Integer(required=True, validate=event_date_validation)
    apply_start_date = fields.Integer(validate=apply_date_validation)
    apply_end_date = fields.Integer(validate=apply_date_validation)

    location = fields.Integer(required=True)
    address = fields.String()
    url = fields.String(validate=validate.URL())

    max_attendees = fields.Integer(validate=validate.Range(min=1, max=999))

    @validates_schema
    def validate_custom_fields(self, data, **kwargs):
        errors = {}

        # apply_datetime (default settings)
        if 'apply_start_date' not in data:
            data['apply_start_date'] = today_timestamp
        if 'apply_end_date' not in data and 'event_start_date' in data:
            data['apply_end_date'] = data['event_start_date']
        
        # event_datetime    
        event_start = data['event_start_date']
        event_end = data['event_end_date']
        apply_start = data['apply_start_date']
        apply_end = data['apply_end_date']

        if event_end < event_start:
            errors['event_end_date'] = ['Event end date must not be before the start date.']

        if apply_end < apply_start:
            errors['apply_end_date'] = ['Apply end date must not be before apply start date.']

        if apply_end > event_start:
            errors['apply_end_date'] = ['Apply end date must not be after event start date.']  
            
        # location
        location = data['location']

        if location == 0 and not data.get('address'):
            errors['address'] = ['Address is required when location is offline']
        if location == 1 and not data.get('url'):
             errors['url'] = ['URL is required when location is online']

        if errors:
            raise ValidationError(errors)