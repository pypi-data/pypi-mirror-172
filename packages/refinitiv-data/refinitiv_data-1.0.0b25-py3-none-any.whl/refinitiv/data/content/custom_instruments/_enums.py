from enum import Enum


class CustomInstrumentTypes(Enum):
    Formula = "formula"
    UDC = "udc"
    Basket = "basket"


class SpreadAdjustmentMethod(Enum):
    CLOSE_TO_CLOSE = "close-to-close"
    OPEN_TO_OPEN = "open-to-open"
    CLOSE_TO_OPEN = "close-to-open"
    CLOSE_TO_OPEN_OLD_GAP = "close-to-open-old-gap"
    CLOSE_TO_OPEN_NEW_GAP = "close-to-open-new-gap"


class VolumeBasedRolloverMethod(Enum):
    VOLUME = "volume"
    OPEN_INTEREST = "openInterest"
    VOLUME_AND_OPEN_INTEREST = "volumeAndOpenInterest"
    VOLUME_OR_OPEN_INTEREST = "volumeOrOpenInterest"


class DayBasedRolloverMethod(Enum):
    DAYS_BEFORE_EXPIRY = "daysBeforeExpiry"
    DAYS_BEFORE_END_OF_MONTH = "daysBeforeEndOfMonth"
    DAYS_AFTER_BEGINNING_OF_MONTH = "daysAfterBeginningOfMonth"
