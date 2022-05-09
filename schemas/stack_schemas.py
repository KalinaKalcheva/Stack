from marshmallow import Schema, fields


class StackPushRequestSchema(Schema):
    value = fields.Number(required=True, description="value")


class StackResponseSchema(Schema):
    message = fields.Str(default='Success')
