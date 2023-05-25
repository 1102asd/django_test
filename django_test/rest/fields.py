from rest_framework.fields import DecimalField


class NormalizedDecimalField(DecimalField):
    # remove trailing zeros on DecimalFields representation
    def quantize(self, value):
        quantized = super().quantize(value)
        return quantized.normalize()