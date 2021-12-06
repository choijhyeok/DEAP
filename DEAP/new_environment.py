import random
import string
import numpy as np
import pandas as pd


class Env(object):
    def __init__(self,
                 n_company=None,
                 max_order=1000,
                 max_items=30,
                 area_size=20,
                 e=0.3):
        """ Create Sample Simulate Environment.

            Args:
                n_company (int): generate n company data. Defaults to None.
                max_order (int): n rows. Defaults to 10000.
                max_items (int): n items. Defaults to 10.
                area_size (int): n areas. Defaults to 20.
                e (float): probability to select the previous item. Defaults to 0.3.

            Returns:
                env object

        """

        self.n_company_ = np.random.randint(2, 7) if n_company is None else n_company
        self.max_order_ = max_order
        self.max_items_ = max_items
        self.area_size_ = area_size
        self.e_ = e

        self.area_list_ = [alpha for alpha in string.ascii_lowercase[:area_size]]
        self.distance_matrix_ = self._generate_area_distance(area_size)
        company_code = [alpha for alpha in string.ascii_uppercase[:self.n_company_]]
        company_list = self._generate_company_list(company_code, max_order)
        item_list = self._generate_item_list(max_items)

        self.data = pd.DataFrame(
            {
                'order_id': self._generate_order_list(max_order),
                'company_code': company_list,
                'product_code': self._generate_product_list(item_list, max_order, e),
                'amount': self._generate_amount_list(max_order),
                'shipping_area': self._generate_shipping_list(self.area_list_, max_order),
                'first_area': self._generate_first_area(company_list),
                'cost': self._generate_cost_list(max_order)})


    def _generate_first_area(self, company_list: list) -> list:
        # 회사 지역(lower company_code)에서 제일 가까운 지역
        return [self.area_list_[np.argsort(self.distance_matrix_[self.area_list_.index(company.lower())])[1]] for company in
                company_list]


    def _generate_area_distance(self, area_size: int) -> list:
        distance_list = np.random.rand(area_size)
        return [np.round(abs(distance_list - dis), 4) for dis in distance_list]


    def _generate_item_list(self, max_items: int) -> list:
        return [''.join(random.choice(string.ascii_letters + string.digits) for i in range(3)).upper() for _ in
                range(max_items)]


    def _generate_order_list(self, max_order: int) -> list:
        return np.random.choice(range(0, 1000 * max_order), size=max_order) + 300000000


    def _generate_company_list(self, company_list: list, max_order: int) -> list:
        return np.random.choice(company_list, size=max_order)


    def _generate_product_list(self, item_list: list, max_order: int, e: float) -> list:
        previous_item = np.random.choice(item_list)
        product_list = [0] * max_order

        for i, _ in enumerate(range(max_order)):
            if np.random.rand() > e: previous_item = np.random.choice(item_list)
            product_list[i] = previous_item

        return product_list


    def _generate_amount_list(self, max_order: int) -> list:
        return np.random.randint(3, 15, size=max_order)


    def _generate_shipping_list(self, area_list: list, max_order: int) -> list:
        return np.random.choice(area_list, size=max_order)


    def _generate_cost_list(self, max_order: int) -> list:
        return np.random.randint(3000, 7000, size=max_order) * 1000


    def get_saving_rate(self, company: str, origin: str, change: str) -> float:
        """ Get saving ratio by distance.

            Args:
                company (str): Comapny name.
                origin (str): Shipping area.
                change (str): Change shipping area.

            Returns:
                saving ratio (float): -1 ~ 1

        """
        distance = self.distance_matrix_[self.area_list_.index(company.lower())]
        origin_distance = distance[self.area_list_.index(origin)]
        change_distance = distance[self.area_list_.index(change)]

        return round(change_distance - origin_distance, 4)

