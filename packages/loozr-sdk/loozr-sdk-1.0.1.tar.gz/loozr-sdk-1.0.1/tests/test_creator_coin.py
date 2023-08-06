import unittest
import time

from loozr_sdk.accounts import NearClient, new_lzr_account, AccountHelper
from loozr_sdk.creator_coin import create_coin, CreatorCoinRouter
from loozr_sdk.utils.format import (
    get_creator_account_id_from_name, yocto_format)
from loozr_sdk.utils.constants import MINIMUM_STORAGE_BALANCE


class CoinTest(unittest.TestCase):
    def test_create_coin(self):
        coin_name = 'my_coin_%s' % int(time.time() * 10_000)
        create_coin(coin_name)

    def test_purchase_curve_func(self):
        current_supply = yocto_format(155.344952441)
        reserve_balance = yocto_format(3748.798188566)
        buy_amount = yocto_format(0.000001206)
        purchase_return = CreatorCoinRouter._calc_polynomial_mint(
            buy_amount, current_supply)
        self.assertEqual(purchase_return, yocto_format(1.6658304957672954e-8))

        bancor_purchase_return = CreatorCoinRouter._calc_bancor_mint(
            buy_amount, reserve_balance, current_supply)
        self.assertEqual(bancor_purchase_return,
                         yocto_format(1.665832953286128e-8))

    def test_buy_and_sell_creator_coin(self):
        coin_name = 'my_coin_%s' % int(time.time() * 10_000)
        create_coin(coin_name)
        coin_id = get_creator_account_id_from_name(coin_name)

        lzr = NearClient()
        account_name = 'test_user-%s' % int(time.time() * 10_000)

        new_account, resp = new_lzr_account(
            lzr.account, account_name)

        account_helper = AccountHelper(lzr.account)
        account_helper.buy_storage(
            new_account.account_id, MINIMUM_STORAGE_BALANCE)
        account_helper.buy_storage(
            coin_id, MINIMUM_STORAGE_BALANCE)

        account_helper = AccountHelper(lzr.account)
        account_helper.transfer_ft(
            9999999999999999000000000, new_account.account_id)

        router = CreatorCoinRouter(coin_id)

        account_helper = AccountHelper(router.account)
        account_helper.buy_storage(
            new_account.account_id, MINIMUM_STORAGE_BALANCE, coin_id)
        new_tokens = router.buy_token(new_account, 9999999999999999000000000,
                                      'dummuft.testnet', 10)
        router.sell_token(new_account.account_id, int(new_tokens))
