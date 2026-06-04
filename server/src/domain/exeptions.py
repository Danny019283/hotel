class DomainError(Exception):
    pass


class ValidationError(DomainError):
    pass


class MappingError(DomainError):
    pass


class BookingRuleError(ValidationError):
    pass


class BookingDatesError(BookingRuleError):
    pass


class BookingAvailabilityError(BookingRuleError):
    pass


class BookingStayError(BookingRuleError):
    pass


class BookingPastDateError(BookingRuleError):
    pass


class BookingOverlapError(BookingRuleError):
    pass


class ClientRuleError(ValidationError):
    pass


class ClientNameError(ClientRuleError):
    pass


class ClientLastNameError(ClientRuleError):
    pass


class ClientEmailError(ClientRuleError):
    pass


class ClientPhoneError(ClientRuleError):
    pass


class RoomRuleError(ValidationError):
    pass


class RoomAvailabilityError(RoomRuleError):
    pass


class RoomPriceError(RoomRuleError):
    pass


class RoomTypeError(RoomRuleError):
    pass


class PaymentMethodRuleError(ValidationError):
    pass


class PaymentMethodNameError(PaymentMethodRuleError):
    pass


class PaymentMethodActiveError(PaymentMethodRuleError):
    pass


class BillRuleError(ValidationError):
    pass


class BillTotalError(BillRuleError):
    pass


class BillTotalMismatchError(BillRuleError):
    pass


class BillDuplicateError(BillRuleError):
    pass


class UserRuleError(ValidationError):
    pass


class UserUsernameError(UserRuleError):
    pass


class UserPasswordHashError(UserRuleError):
    pass


class UserRoleError(UserRuleError):
    pass
