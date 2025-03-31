from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)


class FavouriteSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    tmdb_id = fields.Int(required=True)

class WatchlaterSchema(Schema):
    id = fields.Int(dump_only =True)
    user_id = fields.Int(required=True)
    tmdb_id=fields.Int(required=True)


##instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
favourites_schema = FavouriteSchema(many=True)
watch_later = WatchlaterSchema(many=True)
