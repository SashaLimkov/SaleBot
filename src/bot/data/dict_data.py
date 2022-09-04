from bot.data import text_data as td
from bot.data import list_data as ld
from bot.services.db import settings_user

MAIN_SETTINGS_SEGREGATOR = {
    1: [td.MM_S_CUR, 1, ld.MM_SETTINGS_CURRENCY],
    2: [td.MM_FORMULA, 2, ld.MM_FORMULA],
    3: [td.MM_POST, 1, ld.MM_POST],
    4: [td.MM_INFO, 1, ld.MM_INFO],
    5: [td.MM_SIGN, 1, ld.MM_SIGN],
    6: [td.MM_SH_LINK, 1, ld.MM_SH_LINK],
    7: [td.MM_GET, 1, ld.MM_GET],
    8: [td.MM_ADD_HELPER, 1, ld.MM_ADD_HELPER],
}

INFO_SAVER = {
    1: settings_user.update_product_link_settings_user,
    2: settings_user.update_product_name_settings_user,
    3: settings_user.update_product_price_settings_user,
    4: settings_user.update_product_discount_settings_user,
    5: settings_user.update_product_description_settings_user,
}
