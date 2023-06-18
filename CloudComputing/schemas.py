from marshmallow import Schema, fields, post_dump, validate
from enum import Enum


class TimeStampSchema(Schema):
    # created_at = fields.DateTime(required=True, dump_only=False)
    # updated_at = fields.DateTime(required=True, dump_only=False)
    # deleted_at = fields.DateTime(required=True, dump_only=True)
    pass


class AuthLogoutSchema(TimeStampSchema):
    email = fields.Str(required=True, load_only=True)


class AuthPenggunaSchema(TimeStampSchema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)


class UserPenggunaSchema(AuthPenggunaSchema):
    id = fields.Str(dump_only=True)
    email = fields.Str(required=True)
    photo = fields.Str()
    premium = fields.Boolean(required=False)
    terakhir_login = fields.DateTime(dump_only=True)


class PlainPenggunaSchema(AuthPenggunaSchema):
    id = fields.Str(dump_only=True)
    photo = fields.Str()
    premium = fields.Boolean(required=False)
    token = fields.Str(required=False)
    terakhir_login = fields.DateTime(dump_only=True)


class LahanImageSchema(TimeStampSchema):
    nama = fields.Str(dump_only=True)
    photo = fields.Str(dump_only=True)


from enum import Enum
from marshmallow import fields, Schema


class StatusEnum(Enum):
    PLAN = "plan"
    EXEC = "exec"
    CLOSE = "close"


class BibitSchema(TimeStampSchema):
    id = fields.Str()
    nama = fields.Str(required=True)
    photo = fields.Str(dump_only=True)
    deskripsi = fields.Str()
    harga_beli = fields.Int()
    jenis = fields.Str(validate=validate.OneOf(["sayuran", "buah"]), required=True)
    link_market = fields.Str()


class AktivitasSchema(TimeStampSchema):
    id = fields.Str()
    nama = fields.Str(required=True)
    keterangan = fields.Str()
    pupuk = fields.Int()
    tanggal_aktifitas = fields.DateTime()


class TanamSchema(TimeStampSchema):
    id = fields.Str()
    jarak = fields.Int()
    status = fields.Str(validate=lambda x: x in [s.value for s in StatusEnum])
    tanggal_tanam = fields.DateTime()
    tanggal_panen = fields.DateTime()
    jumlah_panen = fields.Int()
    harga_panen = fields.Int()


class AllTanamSchema(TanamSchema):
    bibit = fields.Nested(BibitSchema, dump_only=True)
    aktivitas = fields.List(fields.Nested(AktivitasSchema), dump_only=True)


class GetLahanSchema(TimeStampSchema):
    id = fields.Str()
    nama = fields.Str(required=True)
    photo = fields.Str(dump_only=True)
    luas = fields.Float(required=True)
    alamat = fields.Str(required=False)
    lat = fields.Float(required=False, allow_none=True)
    lon = fields.Float(required=False, allow_none=True)


class TanamGetLahanSchema(GetLahanSchema):
    tanam = fields.List(fields.Nested(AllTanamSchema), dump_only=True, default=[])
    # tanam = fields.Nested(AllTanamSchema, dump_only=True, default={})


class PostLahanSchema(TimeStampSchema):
    user_id = fields.Str()
    nama = fields.Str(required=True)
    image = fields.Str(dump_only=True)
    luas = fields.Float(required=True)
    alamat = fields.Str(required=False)
    lat = fields.Float(required=False, allow_none=True)
    lon = fields.Float(required=False, allow_none=True)


class PlainLahanSchema(TimeStampSchema):
    id = fields.Str(required=True)
    nama = fields.Str(required=True)
    photo = fields.Str()
    luas = fields.Float(required=True)
    alamat = fields.Str(required=False)
    lat = fields.Float(required=False)
    lon = fields.Float(required=False)


class PostTanamSchema(TimeStampSchema):
    bibit_id = fields.Str()
    lahan_id = fields.Str()


class ExecTanamSchema(TimeStampSchema):
    id = fields.Str()
    jarak = fields.Int()
    tanggal_tanam = fields.Date()


class CloseTanamSchema(TimeStampSchema):
    id = fields.Str()
    tanggal_panen = fields.Date()
    jumlah_panen = fields.Int()
    harga_panen = fields.Int()


class RekomendasiTanamSchema(TimeStampSchema):
    image = fields.Str()


class RekomendasiTanamIotSchema(TimeStampSchema):
    iot_id = fields.Str()


class PostIotSchema(TimeStampSchema):
    iot_id = fields.Str()
    lahan_id = fields.Str()


class PostIotResetSchema(TimeStampSchema):
    id = fields.Str()


class UploadSchema(TimeStampSchema):
    nama = fields.Str(required=True, load_only=True)


class PenggunaSchema(PlainPenggunaSchema):
    lahan = fields.List(fields.Nested(PlainLahanSchema()), dump_only=True)


class LahanSchema(PlainLahanSchema):
    pengguna = fields.Nested(PlainPenggunaSchema(), dump_only=True)


class UserLahanSchema(UserPenggunaSchema):
    lahan = fields.List(fields.Nested(PlainLahanSchema()), dump_only=True)

    @post_dump(pass_many=True)
    def limit_lahan(self, data, many, **kwargs):
        # Batasi jumlah lahan menjadi 5 data
        if many:
            for item in data:
                item["lahan"] = self.filter_lahan(item["lahan"])
        else:
            data["lahan"] = self.filter_lahan(data["lahan"])
        return data

    def filter_lahan(self, lahan_list):
        filtered_lahan = []
        for lahan in lahan_list:
            if not lahan.get("tanam") or lahan["tanam"].get("created_at") is None:
                filtered_lahan.append(lahan)
        return filtered_lahan
