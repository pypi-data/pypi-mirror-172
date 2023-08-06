# calculator
class Calculator:
    """it is a simple calculator which operates sum, subtract, multiply, divide and nthroot"""

    def __init__(self, memory=0):

        self.memory = memory

    def reset_memory(self):
        """
        This function will reset the memory back to zero
        """
        self.memory = 0

        return self.memory

    def add(self, num1, num2=None):
        """
        This function will perform the sum of two numbers
        Parameters:
            num1 : the num1 to add from
            num2 : the num2 is to be added and if left empty it takes last memory
        Returns:
            Total sum : The sum of the provided numbers
        """

        if num2 == None:
            num2 = self.memory
        self.memory = float(num1) + float(num2)
        return self.memory

    def subtract(self, num1, num2=None):

        """
        This function will performs the subtraction of two numbers
        Parameters:
            num1 : The num1 to subtract from
            num2 :  the num2 is to be subtracted and if left empty it takes last memory
        Returns:
            Total subtraction: The subtraction of the provided numbers
        """

        if num2 == None:
            num2 = self.memory
        self.memory = float(num1) - float(num2)
        return self.memory

    def multiply(self, num1, num2=None):
        """
       This function will perform the multiplication of two numbers
        Parameters:
            num1 : The num1 to multiply from
            num2 : The num2 is to be multiplied and if left empty it takes last memory
        Returns:
            Total subtraction: The multiplication of the provided numbers
        """

        if num2 == None:
            num2 = self.memory

        self.memory = float(num1) * float(num2)
        return self.memory

    def division(self, num1, num2=None):

        """
         This function will perform the division of two numbers
        Parameters:
            num1 : The num1 to divide
            num2 : The num2 is to be multiplied and if left empty it takes last memory
        Returns:
           Total division: The division of the provided numbers
        """

        if num2 == None:
            num2 = self.memory

        self.memory = float(num1) / float(num2)
        return self.memory

    def nthroot(self, num1, num2=None):
        """
        This function will performs the nthroot of two numbers
        Parameters:
            num1 : The num1 is the nthroot
            num2 : The num2 is multiplied by 'N'nnumber of times
        Returns:
           Total division : The "nth Root" used n times in a multiplication gives the original value
        """

        if num2 == None:
            num2 = self.memory

        self.memory = pow(num1, (1 / num2))
        return self.memory


cal = Calculator()

cal.add(2, 3)
