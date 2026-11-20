# def find_duplicate_transactions(transaction_ids: list[str]) -> list[str]:
#     dublicate_set = set()
#     seen_set = set()
#     for item in transaction_ids:
#         if item not in seen_set:
#             seen_set.add(item)
#         else:
#             dublicate_set.add(item)
        
#     return list(dublicate_set)

# input_data = ["tx_01", "tx_02", "tx_03", "tx_01", "tx_04", "tx_02", "tx_01"]
# print(f"Сырой список состоит из {len(input_data)} элементов")
# print("Происходит очистка...")
# duplicates = find_duplicate_transactions(input_data)
# print(f"Всего: {len(duplicates)} дубликатов")
# for item in duplicates:
#     print(item)


# def find_frequent_ips(ip_addresses: list[str], threshold: int) -> list[str]:
#     ip_count = {}
    
#     for ip in ip_addresses:
#         ip_count[ip]=ip_count.get(ip, 0) + 1

#     return_list = []
#     for ip, count in ip_count.items():
#         if count > threshold:
#             return_list.append(ip)
        
#     return return_list

# ips = ["192.168.1.1", "10.0.0.1", "192.168.1.1", "172.16.0.1", "192.168.1.1", "10.0.0.1"]
# threshold = 1
# # Результат: ["192.168.1.1", "10.0.0.1"]
# frequent_ips = find_frequent_ips(ips, threshold)
# for item in frequent_ips:
#     print(item)

# def find_two_sum(amounts: list[int], target: int) -> list[int]:
#     seen = {}
#     for current_index, number in enumerate(amounts):
#         target_addition_num = target - number

#         if target_addition_num in seen:
#             return [seen[target_addition_num], current_index]
#         seen[number] = current_index
#     return []
       
# def find_common_users(source_a: list[int], source_b: list[int]) -> list[int]:
#     visited = set(source_a)

#     common_users = set()
#     for user in source_b:
#         if user in visited:
#             common_users.add(user)

#     return list(common_users)

# def find_first_unique_transaction(transactions: list[str]) -> str | None:
#     count_transactions = {}
#     for item in transactions:
#         count_transactions[item] = count_transactions.get(item, 0) + 1

#     for key, val in count_transactions.items():
#         if val == 1:
#             return str(key)

#     return None

# def count_unique_actions(logs: list[tuple[str, str]]) -> dict[str, int]:
#     user_actions = {}
#     for user, action in logs:
#         if user not in user_actions:
#             user_actions[user] = set()
#         user_actions[user].add(action)

#     result_dict ={}
#     for key, val in user_actions.items():
#         result_dict[key] = len(val)
#     return result_dict

# logs = [
#     ("user_1", "login"),
#     ("user_2", "view_cart"),
#     ("user_1", "view_cart"),
#     ("user_1", "login"),       # Дубликат для user_1
#     ("user_3", "purchase"),
#     ("user_2", "view_cart"),   # Дубликат для user_2
#     ("user_1", "purchase")
# ]
# print(count_unique_actions(logs))

# def find_users_with_duplicate_charges(transactions: list[tuple[str, int]]) -> list[str]:
#     clean_transactions = set()
#     duplicate_transactions = set()
#     for user, cost in transactions:
#         pair = user, cost
#         if pair in clean_transactions:
#             duplicate_transactions.add(user)
#         else:
#             clean_transactions.add(pair)
#     return list(duplicate_transactions)

# transactions = [
#     ("alice", 50),
#     ("bob", 100),
#     ("alice", 20),
#     ("alice", 50),      # Повторное списание 50 у alice
#     ("bob", 200),
#     ("charlie", 30),
#     ("bob", 100),       # Повторное списание 100 у bob
#     ("alice", 50)       # Снова 50 у alice (но в ответе alice должна быть 1 раз)
# ]

# # Ожидаемый результат: ["alice", "bob"] (или ["bob", "alice"])
# print(find_users_with_duplicate_charges(transactions))

# def find_top_spender(purchases: list[tuple[str, int]]) -> tuple[str, int] | None:
#     group_by_clients = {}
#     for customer_id, amount in purchases:
#         group_by_clients[customer_id] = group_by_clients.get(customer_id, 0) + amount

#     max_spent = 0
#     top_client = None
#     for customer_id, total_spent in group_by_clients.items():
#         if total_spent > max_spent:
#             max_spent = total_spent
#             top_client = (customer_id, total_spent)

#     return top_client

# purchases = [
#     ("alice", 50),
#     ("bob", 100),
#     ("alice", 70),
#     ("charlie", 80),
#     ("bob", 10),
#     ("alice", 20)
# ]

# Общие суммы трат:
# "alice": 50 + 70 + 20 = 140
# "bob": 100 + 10 = 110
# "charlie": 80

# # Ожидаемый результат:
# # ("alice", 140)
# print(find_top_spender(purchases))

# def find_overdrawn_accounts(transactions: list[tuple[str, str, int]]) -> dict[str, int]:
#     balance = {}
#     for account_id, operation_type, amount in transactions:
#         if operation_type == "DEPOSIT":
#             balance[account_id] = balance.get(account_id, 0) + amount
#             continue
#         elif operation_type == "WITHDRAW":
#             balance[account_id] = balance.get(account_id, 0) - amount 
#     negative_balance = {}
#     for user, total in balance.items():
#         if total < 0:
#             negative_balance[user] = total
#     return negative_balance
# transactions = [
#     ("acc_1", "DEPOSIT", 100),
#     ("acc_2", "DEPOSIT", 50),
#     ("acc_1", "WITHDRAW", 120),  # Баланс acc_1: 100 - 120 = -20
#     ("acc_3", "DEPOSIT", 30),
#     ("acc_2", "WITHDRAW", 40),   # Баланс acc_2: 50 - 40 = 10
#     ("acc_3", "WITHDRAW", 50),   # Баланс acc_3: 30 - 50 = -20
#     ("acc_4", "DEPOSIT", 10),
#     ("acc_4", "WITHDRAW", 10)    # Баланс acc_4: 10 - 10 = 0 (не овердрафт)
# ]

# Ожидаемый результат:
# {
#     "acc_1": -20,
#     "acc_3": -20
# }
# print(find_overdrawn_accounts(transactions))


# def find_two_sum_sorted(amounts: list[int], target: int) -> list[int]:
#     left = 0
#     right = len(amounts)-1
#     while left < right:
#         left_plus_right = amounts[left] + amounts[right]
#         if left_plus_right == target:
#             return [left, right]
#         elif left_plus_right > target:
#             right -= 1
#         elif left_plus_right < target:
#             left +=1
#     return[]
# amounts = [2, 7, 11, 15]
# target = 9
# print(find_two_sum_sorted(amounts,target))

# def is_palindrome(s: str) -> bool:
#     left = 0
#     right = len(s) - 1
#     while left < right:
#         if s[left].lower() == s[right].lower():
#             left+=1
#             right-=1
#         else:
#             return False
#     return True



# def max_traffic_window(traffic: list[int], k: int) -> int:
#     initial_sum = 0
#     for i in range(k):
#         initial_sum += traffic[i]

#     max_sum = initial_sum

#     for i in range(k, len(traffic)):
#         initial_sum = (initial_sum - traffic[i-k]) + traffic[i]
#         if initial_sum > max_sum :
#             max_sum = initial_sum
            
#     return max_sum

# traffic = [2, 1, 5, 1, 3, 2]
# k = 3
# print(max_traffic_window(traffic, k))



# def min_subarray_len(target: int, nums: list[int]) -> int:
#     left = 0
#     current_sum = 0
#     min_len = float('inf')
#     for right in range(len(nums)):
#         current_sum+=nums[right]
#         while current_sum >=target:
#             min_len = min(min_len, right + 1 -left)
#             current_sum-=nums[left]
#             left+=1
#     if min_len < float('inf'):
#         return min_len
#     return 0
            
# target = 7
# nums = [2, 3, 1, 2, 4, 3]

# # Подмассивы с суммой >= 7:
# # [2, 3, 1, 2] -> сумма 8, длина 4
# # [3, 1, 2, 4] -> сумма 10, длина 4
# # [1, 2, 4]    -> сумма 7, длина 3
# # [4, 3]       -> сумма 7, длина 2  <-- МИНИМУМ

# # Результат: 2
# print(min_subarray_len(target, nums))

# set vs dict
# def length_of_longest_substring(s: str) -> int:
#     left = 0
#     unique_characters = set()
#     max_len = 0
#     for right in range(len(s)):
#         char = s[right]
#         while char in unique_characters:
#             unique_characters.remove(s[left])
#             left +=1
#         unique_characters.add(char)
#         max_len = max(max_len, len(unique_characters))
        
#     return max_len
# def length_of_longest_substring(s: str) -> int:
#     left = 0
#     unique_characters = {}
#     max_len = 0
#     for right in range(len(s)):
#         if s[right] in unique_characters:
#             left = max(left, unique_characters.get(s[right]) + 1)
            
#         unique_characters[s[right]] = right 
#         max_len = max(max_len, right - left + 1)
#     return max_len, unique_characters

# print(length_of_longest_substring(s = "abba"))

# def longest_ones(nums: list[int], k: int) -> int:
#     left = 0
#     longest_subsequense = {}
#     max_len = 0
#     for right in range(len(nums)):
#         longest_subsequense[nums[right]] = longest_subsequense.get(nums[right], 0) + 1
#         if longest_subsequense.get(0, 0)>k:
#             longest_subsequense[nums[left]] = longest_subsequense.get(nums[left]) - 1
#             left +=1
#         max_len = max(max_len, right - left + 1)
#     return max_len

# def longest_ones(nums: list[int], k: int) -> int:
#     count_zero = 0
#     left = 0
#     max_len = 0
#     for right in range(len(nums)):
#         if nums[right]==0:
#             count_zero+=1
#         while count_zero>k:
#             if nums[left] ==0:
#                 count_zero-=1
#             left+=1

#         max_len=max(max_len,right-left+1)
#     return max_len
        
# nums = [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1]
# k =  3
# print(longest_ones(nums, k))    
#      
# def total_fruit(fruits: list[int]) -> int:
#     left = 0
#     current_state = {}
#     max_len = 0
#     for right in range(len(fruits)):
#         current_state[fruits[right]] = current_state.get(fruits[right], 0) + 1
#         while len(current_state)>2:
#             current_state[fruits[left]]-=1
#             if current_state[fruits[left]] == 0:
#                 current_state.pop(fruits[left])
#             left+=1
        
#         max_len = max(max_len, right - left + 1)
#     return max_len

# fruits = [1, 2, 3, 2, 2]
# print(total_fruit(fruits))


# def maximumUniqueSubarray(nums: list[int]) -> int:
#     left = 0
#     max_subaray = set()
#     max_sum = 0
#     current_sum = 0
#     for right in range(len(nums)):
#         elem = nums[right]
#         while elem in max_subaray:
#             current_sum-=nums[left]
#             max_subaray.remove(nums[left])
#             left+=1
#         max_subaray.add(elem)
#         current_sum+=nums[right]
#         max_sum = max(max_sum,current_sum)
#     return max_sum


# print(maximumUniqueSubarray(nums = [4,2,4,5,6]))


        
# def maxSubarrayLength(nums: list[int], k: int) -> int:
#     left = 0
#     freq_count = {}
#     max_len = 0
#     cur_len = 0
#     for right in range(len(nums)):
#         freq_count[nums[right]] = freq_count.get(nums[right], 0) + 1
#         while freq_count[nums[right]]>k:
#             freq_count[nums[left]]-=1
#             cur_len-=1
#             left+=1
#         cur_len += 1
#         max_len = max(max_len, cur_len)
#     return max_len
            

# print(maxSubarrayLength(nums = [1, 2, 1, 2, 1, 2, 1, 2], k = 1))

        
# def numSubarrayProductLessThanK(nums: list[int], k: int) -> int:
#     if k <= 1:
#        return 0
#     left = 0
#     cur_product = 1
#     amount = 0
#     for right in range(len(nums)):
#         cur_product*=nums[right]
#         while cur_product >= k:
#             cur_product = cur_product // nums[left]
#             left += 1
#         amount += right - left + 1
#     return amount
                
# print(numSubarrayProductLessThanK(nums = [10, 5, 2, 6], k = 100))
# 1+ 2 + 3 + 3

# def equalSubstring(s: str, t: str, maxCost: int) -> int:
#     left = 0
#     max_cost = 0
#     cur_cost = 0
#     for right in range(len(s)):
#         difference = abs(ord(s[right]) - ord(t[right]))
#         cur_cost+=difference
#         while cur_cost > maxCost:
#             cur_cost= cur_cost - abs(ord(s[left]) - ord(t[left]))
#             left +=1
#         max_cost = max(max_cost, right-left+1)
#     return max_cost
# print(equalSubstring(s = "abcd", t = "bcdf", maxCost = 3))

# def maxVowels(s: str, k: int) -> int:
#     vowels = set("aeiou")
#     max_len = 0
#     for i in range(k):
#         if s[i] in vowels:
#             max_len+=1
#     cur_len = max_len        
#     for index in range(k, len(s)):
#         if s[index] in vowels:
#             cur_len+=1
#         if s[index-k] in vowels:
#             cur_len-=1
#         max_len = max(max_len,cur_len)
#     return max_len
# print(maxVowels(s = "abciiidef", k = 3))

# class NumArray:

#     def __init__(self, nums: list[int]):
#         self.prefix = self._build_prefix(nums)

#     def _build_prefix(self, nums: list[int]) ->:
#         n = len(nums)
#         prefix = [0] * (n+1)
#         for i in range(n):
#             prefix[i+1] = prefix[i] + nums[i]
#         return prefix

    # def sumRange(self, left: int, right: int) -> int:
    #     return self.prefix[right - 1] - self.prefix[left]

# class NumMatrix:

#     def __init__(self, matrix: list[list[int]]):
#         self.cols = len(matrix[0])
#         self.rows = len(matrix)
#         self.prefix = [[0] * (self.cols + 1) for _ in range(self.rows+1)]
#         self.fillPrefix(matrix)

#     def fillPrefix(self, matrix: list[list[int]]):

#         for i in range(1,self.rows+1):
#             for j in range(1,self.cols+1):

#                 self.prefix[i][j] = (matrix[i-1][j-1]+self.prefix[i][j-1]+self.prefix[i-1][j]-self.prefix[i-1][j-1])

#     def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        
#         return (self.prefix[row2+1][col2+1]-self.prefix[row1][col2+1]-self.prefix[row2+1][col1]+self.prefix[row1][col1]
#     )
       
        
            
def lengthOfLongestSubstring(s: str) -> int:
    left = 0
    max_len = 0
    cur_len = 0
    cur_substring = set()
    for right in range(len(s)):
        while s[right] in cur_substring:
            cur_substring.remove(s[left])
            left+=1
        cur_len = right - left + 1
        cur_substring.add(s[right])
        max_len = max(max_len, cur_len)
    return max_len


    
    
