class PrimeChecker:
    def __init__(self, prime_list):
        self.starting_prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.prime_list = prime_list
        self.end_digit_fail_list = [0, 2, 4, 5, 6, 8]

    def digit_sum(self, number):
        """
        Function to determine the sum of the digits of the number passed to it.
        """
        return sum(int(digit) for digit in str(number))

    def digit_sum_check(self, number):
        """
        Function to determine the sum of the digits of the number. If the sum of the digits are divisible by 3, then the number will be divisible by 3.
        """
        return self.digit_sum(number) % 3 != 0

    def last_digit(self, number):
        """
        Function to check the last digit of the number. If the last digit of a number is in [0,2,4,5,6,8], then it can't be prime because it's either even, or is divisible by 5. The only exception to this is 2, which while even, is prime since it's only factors are 1 and 2.
        """
        return int(str(number)[-1:]) not in self.end_digit_fail_list

    def seven_check(self, number):
        """
        Function to check for the divisible by 7 condition. In this case, it's easier to give an example. Take 161. If we take it's last digit (1), double it (1*2=2), then subtract that from the number not including the last digit (161 becomes 16), which gives us 16-2=14, then take that result (14) and we can divide it evenly by 7 (in this case, 14/7=2), then the original number (161) is also evenly divisible by 7. This is always the case.
        """
        last_digit = int(str(number)[-1:])
        new_number_1 = int(str(number)[:-1])
        new_number_2 = new_number_1 - (2 * last_digit)
        return new_number_2 % 7 != 0

    def eleven_check(self, number):
        """
        Function to check for the divisible by 11 condition. This condition is best explained with an example. Take the number 574652. If we take the sums of alternating digits (5+4+5=14 and 7+6+2=15), then we take the absolute value of their difference (|14-15|=1), and that value is divisible by 11, then the original number is divisible by 11. In this case, 1 is not divisble by 11, so 574652 passes this check.
        """
        new_number_1 = self.digit_sum(int(str(number)[0::2]))
        new_number_2 = self.digit_sum(int(str(number)[1::2]))
        return abs(new_number_1 - new_number_2) % 11 != 0

    def semiprime_and_squarefree_prime_check(self, number):
        """
        Function to check for Semiprimes and Squarefree Primes. Semiprimes are numbers that are squares of other primes. For example, 169 is the square of 13. Squarefree primes are numbers that are the product of other primes. For example, 221 is the product of 13 and 17. We can check for both these conditions in the same manner. If the number we're checking, mod a known prime (161 % 13), equals 0, then the number is either a semiprime or squarefree prime. We also only need to check up to known primes of less than or equal to the square root of the number we're checking since in either case, a factor of a semiprime or a squarefree prime will always be equal to or less than the square root of the number.
        """
        square_root = number**0.5
        for prime in self.prime_list:
            if square_root < prime:
                break
            if number % prime == 0:
                return False
        return True

    def prime_check(self, number):
        """
        Function to determine if a number is Prime or not. It runs through all the checks and then returns if the number is prime or not.
        """
        if number in self.starting_prime_list:
            return True
        if not self.last_digit(number):
            return False
        if not self.digit_sum_check(number):
            return False
        if not self.seven_check(number):
            return False
        if not self.eleven_check(number):
            return False
        return self.semiprime_and_squarefree_prime_check(number)
