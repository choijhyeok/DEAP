import random
import numpy as np
import pandas as pd

class Knapsack01Problem:

    def __init__(self):

        # initialize instance variables:
        self.items = []
        self.maxCapacity = 0
        self.budget = 0
        self.load_dataset = True
        self.df = []

        # initialize the data:
        self.__initData()

    def __len__(self):
        """
        :return: the total number of items defined in the problem
        """
        return len(self.items)

    def __initData(self):

        self.maxCapacity = 250
        self.budget = 10000000


        
    def getItems(self,data):
        
        self.items = data
    

    # ----------------- value만 -----------------------#
    def getValue_v(self, float_list):    

        best_value = best_order_id = 0

        for i in range(len(float_list)):
            order_id,value = self.items[i]
    
            if best_value > int(float_list[i] * value):
                best_value = int(float_list[i] * value)
                best_order_id = order_id
                
                
        return best_value
    
    
    def printItems_v(self, float_list):

        best_value = best_order_id = 0
        for i in range(len(float_list)):
            order_id,value = self.items[i]
             
            if(best_value > int(float_list[i] * value) and int(float_list[i] * value) <  0):    
                best_value = int(float_list[i] * value)
                best_order_id = order_id

#                 print("- Adding {} , value : {}".format(order_id,value))
        
        print('best는 order_id : {} , value : {}'.format(best_order_id,best_value))
        
    # ----------------- value만 -----------------------#
    
    

    
    
    # ----------------- weight만 -----------------------#
    def getValue_w(self, float_list):    

        totalWeight = best_order_id = 0

        for i in range(len(float_list)):
            order_id,weight = self.items[i]
    
            if totalWeight + int(float_list[i] * weight) <= self.maxCapacity:
                totalWeight += int(float_list[i] * weight)
                best_order_id = order_id
                
                
        return totalWeight
    
    
    def printItems_w(self, float_list):

        totalWeight = best_order_id = 0
        for i in range(len(float_list)):
            order_id,weight = self.items[i]
            
            if totalWeight + int(float_list[i] * weight) <= self.maxCapacity:
                if int(float_list[i] * weight) >= 0:
                    totalWeight += int(float_list[i] * weight)
                    best_order_id = order_id
                    print("- Adding {} , weight : {}, accumulated weight = {}".format(order_id,weight,totalWeight))

        
        print('total weight : {}'.format(totalWeight))
        
    # ----------------- weight만 -----------------------#
    
    

    
    
    # ----------------- cost만 -----------------------#
    def getValue_c(self, float_list):    

        totalCost = best_order_id = 0
        
        for i in range(len(float_list)):
            order_id,cost = self.items[i]
             
            if(totalCost + int(float_list[i] * cost) <= self.budget and int(float_list[i] * cost) >= 0):
                totalCost += int(float_list[i] * cost)
                best_order_id = order_id
                
                
                
        return totalCost
    
    
    
    def printItems_c(self, float_list):

        totalCost = best_order_id = 0
        for i in range(len(float_list)):
            order_id,cost = self.items[i]
             
            if totalCost + int(float_list[i] * cost) <= self.budget:
                if int(float_list[i] * cost) >= 0:
                    totalCost += int(float_list[i] * cost)
                    best_order_id = order_id
                    print("- Adding {} , cost : {}, accumulated cost = {}".format(order_id,cost,totalCost))

        
        print('best cost : {}'.format(totalCost))
        
    # ----------------- cost만 -----------------------#
    
    
    
#     # ----------------- all -----------------------#
#     def getValue_all(self, float_list):    

#         totalWeight =  totalCost = 0
#         totalValue = 0
        
#         for i in range(len(float_list)):
#             order_id,cost,value,weight = self.items[i]
            
#             if (totalCost += int(float_list[i] * cost) <= self.budget & totalWeight += int(float_list[i] * weight) <= self.maxCapacity:
                
#                 totalCost += int(float_list[i] * cost)
#                 totalWeight += int(float_list[i] * weight)
#                 totalValue += int(float_list[i] * value)
                
#         return totalCost
    
    
    
#     def printItems_c(self, float_list):

#         totalCost = best_order_id = 0
#         for i in range(len(float_list)):
#             order_id,cost = self.items[i]
             
#             if totalCost + int(float_list[i] * cost) <= self.budget:
#                 if int(float_list[i] * cost) >= 0:
#                     totalCost += int(float_list[i] * cost)
#                     best_order_id = order_id
#                     print("- Adding {} , cost : {}, accumulated cost = {}".format(order_id,cost,totalCost))

        
#         print('best cost : {}'.format(best_order_id,totalCost))
        
#     # ----------------- cost만 -----------------------#
    
    
    
    
    
    
    # ---------------- weight,cost,value 전체 ------------------ #
    def getValue_all(self, float_list):
        
        totalWeight = totalValue = 0
        totalCost = 0
    
        for i in range(len(float_list)):
            order_id, cost, value, weight = self.items[i]
            if totalWeight + int(float_list[i] * weight) <= self.maxCapacity and totalCost + int(float_list[i] * cost) <= self.budget:
                
                totalWeight += int(float_list[i] * weight)
                totalCost += int(float_list[i] * cost)
                totalValue += int(float_list[i] * value)
        
        return totalWeight
    
    
    
    def printItems_all(self, float_list):
        

        totalWeight = totalValue = 0
        totalCost = 0

        for i in range(len(float_list)):
            order_id, cost, value, weight = self.items[i]
            if totalWeight + int(float_list[i] * weight) <= self.maxCapacity and int(float_list[i] * weight) >= 0 \
                    and totalCost + int(float_list[i] * cost) <= self.budget:

                totalWeight += int(weight * float_list[i])
                totalCost += int(cost * float_list[i])
                totalValue += int(value * float_list[i]) 

                print("- Adding {}: "
                      "weight = {}, "
                      "value = {}, "
                      "cost = {}, "
                      "portion = {}, "
                      "accumulated weight = {}, "
                      "accumulated value = {}, "
                      "total cost = {}".format(order_id, weight, value, cost, float_list[i], totalWeight, totalValue,
                                               totalCost))
        print("- Total weight = {}, Total value = {}, Total cost = {}".format(totalWeight, totalValue, totalCost))
        
    # ---------------- weight,cost,value 전체 ------------------ #
    
    
    
    
#     def getValue(self, float_list):
    

#         totalWeight = totalValue = 0
#         totalCost = 0

#         for i in range(len(float_list)):
#             item, weight, value, cost = self.items[i]
#             if totalWeight + int(float_list[i] * weight) <= self.maxCapacity and int(float_list[i] * weight) >= 0 \
#                     and totalCost + int(float_list[i] * cost) <= self.budget:
#                 totalWeight += int(float_list[i] * weight)
#                 totalCost += int(float_list[i] * cost)
#                 totalValue += int(float_list[i] * value) - totalCost
#         return totalValue


# testing the class:
def main():
    # create a problem instance:
    knapsack = Knapsack01Problem()

    # creaete a random solution and evaluate it:
    randomSolution = np.random.randint(2, size=len(knapsack))
    print("Random Solution = ")
    print(randomSolution)
    knapsack.printItems(randomSolution)


if __name__ == "__main__":
    main()