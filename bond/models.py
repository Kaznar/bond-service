from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import (
    ForeignKey, CharField, DecimalField, DateField, CASCADE
)
from django.utils import timezone

from bond_service.base.mixins import ActiveMixin
from bond_service.base.models import BaseModel
from bond_service.base.validators import validator_isin, validator_interest_rate
from user.models import User


class Bond(BaseModel, ActiveMixin):
    user = ForeignKey(User, on_delete=CASCADE)
    name = CharField(max_length=255)
    isin = CharField(
        max_length=12,
        unique=True,
        db_index=True,
        validators=[validator_isin],
        help_text="The ISIN (International Securities Identification Number) of the bond."
    )
    value = DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="The value of the bond. Must be a positive number."
    )
    interest_rate = DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[validator_interest_rate],
        help_text="The interest rate of the bond in percent (0-100%)."
    )
    purchase_date = DateField()
    maturity_date = DateField()
    interest_payment_frequency = CharField(max_length=50)

    def __str__(self):
        return self.name

    def clean(self):
        if self.purchase_date > self.maturity_date:
            raise ValidationError('Maturity date must be later than purchase date.')

    @property
    def future_value(self) -> Decimal | None:
        if self.purchase_date and self.maturity_date:
            # https://www.wallstreetprep.com/knowledge/future-value-fv/
            days_to_maturity = (self.maturity_date - timezone.now().date()).days
            ytm = Decimal(days_to_maturity) / Decimal('365')
            interest_rate_decimal = self.interest_rate / Decimal('100')
            future_value = self.value * ((Decimal('1') + interest_rate_decimal) ** ytm)
            return future_value.quantize(Decimal('0.01'))

        return None
