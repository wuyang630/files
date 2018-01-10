from peewee import *

database_proxy = Proxy()

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database_proxy

class AuthGroup(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'auth_group'

class DjangoContentType(BaseModel):
    app_label = CharField()
    model = CharField()

    class Meta:
        db_table = 'django_content_type'
        indexes = (
            (('app_label', 'model'), True),
        )

class AuthPermission(BaseModel):
    codename = CharField()
    content_type = ForeignKeyField(db_column='content_type_id', rel_model=DjangoContentType, to_field='id')
    name = CharField()

    class Meta:
        db_table = 'auth_permission'
        indexes = (
            (('content_type', 'codename'), True),
        )

class AuthGroupPermissions(BaseModel):
    group = ForeignKeyField(db_column='group_id', rel_model=AuthGroup, to_field='id')
    permission = ForeignKeyField(db_column='permission_id', rel_model=AuthPermission, to_field='id')

    class Meta:
        db_table = 'auth_group_permissions'
        indexes = (
            (('group', 'permission'), True),
        )

class AuthUser(BaseModel):
    date_joined = DateTimeField()
    email = CharField()
    first_name = CharField()
    is_active = BooleanField()
    is_staff = BooleanField()
    is_superuser = BooleanField()
    last_login = DateTimeField(null=True)
    last_name = CharField()
    password = CharField()
    username = CharField(unique=True)

    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(BaseModel):
    group = ForeignKeyField(db_column='group_id', rel_model=AuthGroup, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'auth_user_groups'
        indexes = (
            (('user', 'group'), True),
        )

class AuthUserUserPermissions(BaseModel):
    permission = ForeignKeyField(db_column='permission_id', rel_model=AuthPermission, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'auth_user_user_permissions'
        indexes = (
            (('user', 'permission'), True),
        )

class DjangoAdminLog(BaseModel):
    action_flag = IntegerField()
    action_time = DateTimeField()
    change_message = TextField()
    content_type = ForeignKeyField(db_column='content_type_id', null=True, rel_model=DjangoContentType, to_field='id')
    object = TextField(db_column='object_id', null=True)
    object_repr = CharField()
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'django_admin_log'

class DjangoMigrations(BaseModel):
    app = CharField()
    applied = DateTimeField()
    name = CharField()

    class Meta:
        db_table = 'django_migrations'

class DjangoSession(BaseModel):
    expire_date = DateTimeField(index=True)
    session_data = TextField()
    session_key = CharField(primary_key=True)

    class Meta:
        db_table = 'django_session'

class ShopArea(BaseModel):
    category = IntegerField()
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    name = CharField()
    updated = DateTimeField()

    class Meta:
        db_table = 'shop_area'

class FlowFlow(BaseModel):
    area = ForeignKeyField(db_column='area_id', rel_model=ShopArea, to_field='id')
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    flow_in = IntegerField()
    flow_out = IntegerField()
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    time = DateTimeField()
    updated = DateTimeField()

    class Meta:
        db_table = 'flow_flow'

class FlowFlowreport(BaseModel):
    area = ForeignKeyField(db_column='area_id', rel_model=ShopArea, to_field='id')
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    flow_in = IntegerField()
    flow_out = IntegerField()
    hour = DateTimeField(db_column='hour_id', null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    updated = DateTimeField()

    class Meta:
        db_table = 'flow_flowreport'

class HeatmapHeatmapreport(BaseModel):
    area = ForeignKeyField(db_column='area_id', rel_model=ShopArea, to_field='id')
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    hot = IntegerField()
    hour = DateTimeField(db_column='hour_id', null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    updated = DateTimeField()

    class Meta:
        db_table = 'heatmap_heatmapreport'

class ShopFloor(BaseModel):
    building = CharField()
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    name = CharField()
    plan = CharField(null=True)
    ratio = FloatField()
    updated = DateTimeField()

    class Meta:
        db_table = 'shop_floor'

class ShopCamera(BaseModel):
    background = CharField(null=True)
    category = IntegerField()
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    enable = BooleanField()
    floor = ForeignKeyField(db_column='floor_id', null=True, rel_model=ShopFloor, to_field='id')
    floor_x = FloatField()
    floor_y = FloatField()
    h = IntegerField()
    id = CharField(primary_key=True)
    ip = CharField()
    is_deleted = BooleanField()
    mac = CharField()
    name = CharField()
    ratio = FloatField()
    rtsp = CharField()
    updated = DateTimeField()
    w = IntegerField()

    class Meta:
        db_table = 'shop_camera'

class ShopRectangle(BaseModel):
    area = ForeignKeyField(db_column='area_id', null=True, rel_model=ShopArea, to_field='id')
    camera = ForeignKeyField(db_column='camera_id', null=True, rel_model=ShopCamera, to_field='id')
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    h = IntegerField()
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    updated = DateTimeField()
    w = IntegerField()
    x = IntegerField()
    y = IntegerField()

    class Meta:
        db_table = 'shop_rectangle'

class HeatmapHeatvalue(BaseModel):
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    hot = IntegerField()
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    rect = ForeignKeyField(db_column='rect_id', rel_model=ShopRectangle, to_field='id')
    time = DateTimeField()
    updated = DateTimeField()
    x = IntegerField()
    y = IntegerField()

    class Meta:
        db_table = 'heatmap_heatvalue'

class HeatmapStaymapreport(BaseModel):
    area = ForeignKeyField(db_column='area_id', rel_model=ShopArea, to_field='id')
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    hour = DateTimeField(db_column='hour_id', null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    stay = IntegerField()
    updated = DateTimeField()

    class Meta:
        db_table = 'heatmap_staymapreport'

class HeatmapStayvalue(BaseModel):
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    rect = ForeignKeyField(db_column='rect_id', rel_model=ShopRectangle, to_field='id')
    stay = IntegerField()
    time = DateTimeField()
    updated = DateTimeField()
    x = IntegerField()
    y = IntegerField()

    class Meta:
        db_table = 'heatmap_stayvalue'

class PeoplePeoplereport(BaseModel):
    age_cat1 = IntegerField()
    age_cat2 = IntegerField()
    age_cat3 = IntegerField()
    age_cat4 = IntegerField()
    age_cat5 = IntegerField()
    age_cat6 = IntegerField()
    age_cat7 = IntegerField()
    age_cat8 = IntegerField()
    area = ForeignKeyField(db_column='area_id', rel_model=ShopArea, to_field='id')
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    gender_female = IntegerField()
    gender_male = IntegerField()
    hour = DateTimeField(db_column='hour_id', null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    updated = DateTimeField()

    class Meta:
        db_table = 'people_peoplereport'

class PeoplePerson(BaseModel):
    age = IntegerField()
    area = ForeignKeyField(db_column='area_id', rel_model=ShopArea, to_field='id')
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    gender = IntegerField()
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    time = DateTimeField()
    updated = DateTimeField()

    class Meta:
        db_table = 'people_person'

class ShopSpu(BaseModel):
    attr = CharField()
    brand = CharField()
    category = CharField()
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    manufacturer = CharField()
    name = CharField()
    updated = DateTimeField()

    class Meta:
        db_table = 'shop_spu'

class ShopSku(BaseModel):
    code = CharField()
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    package = CharField()
    price = DecimalField()
    sku_attr = CharField()
    spu = ForeignKeyField(db_column='spu_id', null=True, rel_model=ShopSpu, to_field='id')
    updated = DateTimeField()

    class Meta:
        db_table = 'shop_sku'

class ProductProductreport(BaseModel):
    clicks = IntegerField()
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    hour = DateTimeField(db_column='hour_id', null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    sku = ForeignKeyField(db_column='sku_id', rel_model=ShopSku, to_field='id')
    updated = DateTimeField()
    views = IntegerField()

    class Meta:
        db_table = 'product_productreport'

class ShopShelf(BaseModel):
    area = ForeignKeyField(db_column='area_id', null=True, rel_model=ShopArea, to_field='id')
    category = IntegerField()
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    layers = IntegerField()
    name = CharField()
    updated = DateTimeField()

    class Meta:
        db_table = 'shop_shelf'

class ProductShelfview(BaseModel):
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    shelf = ForeignKeyField(db_column='shelf_id', rel_model=ShopShelf, to_field='id')
    time = DateTimeField()
    updated = DateTimeField()
    views = IntegerField()

    class Meta:
        db_table = 'product_shelfview'

class ProductSkuclick(BaseModel):
    clicks = IntegerField()
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    sku = ForeignKeyField(db_column='sku_id', rel_model=ShopSku, to_field='id')
    time = DateTimeField()
    updated = DateTimeField()

    class Meta:
        db_table = 'product_skuclick'

class ShopPosition(BaseModel):
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    layer = IntegerField()
    shelf = ForeignKeyField(db_column='shelf_id', null=True, rel_model=ShopShelf, to_field='id')
    sku = ForeignKeyField(db_column='sku_id', null=True, rel_model=ShopSku, to_field='id')
    slot = IntegerField()
    updated = DateTimeField()

    class Meta:
        db_table = 'shop_position'

class ShopVenue(BaseModel):
    address = CharField()
    created = DateTimeField()
    deleted_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    is_deleted = BooleanField()
    name = CharField()
    updated = DateTimeField()

    class Meta:
        db_table = 'shop_venue'

class SqliteSequence(BaseModel):
    name = UnknownField(null=True)  # 
    seq = UnknownField(null=True)  # 

    class Meta:
        db_table = 'sqlite_sequence'
        primary_key = False

