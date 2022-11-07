class Solution:
    def getImportance(self, employees: List['Employee'], id: int) -> int:
        
        all_employees = {}
        
        for employee in employees:
            all_employees[employee.id] = employee
            
        def get_sum(employee_id: int):
            final_sum = all_employees[employee_id].importance
            for subordinate_id in all_employees[employee_id].subordinates:
                final_sum += get_sum(subordinate_id)
            return final_sum
            
        return get_sum(id)
