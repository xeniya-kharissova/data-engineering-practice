# class CoffeeOrder:
#     def __init__(self, item_name : str, price : float, count : int):
#         self.item_name = self._clean_name(item_name)
#         self.price = price
#         self.count = count
#     def _clean_name(self, raw_name : str) -> str:
#         return raw_name.strip().upper()
#     def get_total(self, discount : float = 0.00) -> float :
#         total_price = self.price * self.count
#         if discount > 0:
#             total_price *=(1-discount)
#         return total_price

# order = CoffeeOrder("   latte   ", 250.0, 1)
# print(order.item_name)

# class NumArray:

#     def __init__(self, nums: list[int]):
#         self.prefix = self._create_prefix(nums)

#     def _create_prefix(self, initial_array):
#         pref = [0] * (len(initial_array)+1)
#         for i in range(1, len(initial_array) + 1):
#             pref[i] = pref[i-1] + initial_array[i-1]
#         return pref

#     def sumRange(self, left: int, right: int) -> int:
#         return self.prefix[right+1] - self.prefix[left]
        
# num_array = NumArray([-2, 0, 3, -5, 2, -1])
# print(num_array.sumRange(0,2))

from dataclasses import dataclass

@dataclass
class Order:
    item_name : str
    client_name : str
    price : float
    count : int

    def calculate_total(self):
        return self.price*self.count

# order = Order("LATTE", "Алексей", 250.0, 2)
# print(order)
# print(order.calculate_total())


# from dataclasses import dataclass

@dataclass
class DeliveryOrder(Order):
    
    delivery_fee: float

    def calculate_total(self):
        return super().calculate_total() + self.delivery_fee
    
order = DeliveryOrder("CAPPUCCINO", "Мария", 300.0, 1, 150)
print(order.calculate_total())
