import time

class GF2_191:
    def __init__(self):
        self.m = 191

    def bin_to_list(self, bin_str):
        return [int(b) for b in bin_str]

    def list_to_bin(self, bin_list):
        return ''.join(map(str, bin_list))

    def add(self, a, b):
        if len(a) != len(b):
            raise ValueError("Елементи повинні мати однакову довжину.")
        return [ai ^ bi for ai, bi in zip(a, b)]

    def cyclic_shift_left(self, number, i):
        i = i % len(number)
        return number[i:] + number[:i]

    def cyclic_shift_right(self, number, i):
        i = i % len(number)
        return number[-i:] + number[:-i]

    def build_lambda_matrix(self, m, p):
        Lambda = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                if (pow(2, i, p) + pow(2, j, p)) % p == 1 or \
                   (pow(2, i, p) - pow(2, j, p)) % p == 1 or \
                   -(pow(2, i, p) + pow(2, j, p)) % p == 1 or \
                   -(pow(2, i, p) - pow(2, j, p)) % p == 1:
                    Lambda[i][j] = 1
        return Lambda

    def multiply(self, a, b):
        if len(a) != self.m or len(b) != self.m:
            raise ValueError("Довжина елементів повинна дорівнювати m.")

        p = 2 * self.m + 1
        Lambda = self.build_lambda_matrix(self.m, p)
        result = [0] * self.m

        for i in range(self.m):
            u_shift = self.cyclic_shift_left(a, i)
            v_shift = self.cyclic_shift_left(b, i)
            result[i] = sum([u_shift[j] * Lambda[j][k] * v_shift[k] for j in range(self.m) for k in range(self.m)]) % 2

        return result

    def trace(self, y):
        return sum(y) % 2

    def square(self, y):
        return self.cyclic_shift_right(y, 1)

    def inverse(self, a):
        c = a
        k = 1
        m = bin(self.m - 1).lstrip("0b")
        t = len(m)

        for i in range(1, t):
            d = c
            for p in range(k):
                d = self.square(d)
            c = self.multiply(d, c)
            k = k * 2

            if m[i] == "1":
                c = self.multiply(self.square(c), a)
                k = k + 1

        return self.square(c)

    def power(self, a, n):
        c = [1] * (self.m)
        for i in range(len(n) - 1, -1, -1):
            if n[i] == 1:
                c = self.multiply(c, a)
            a = self.square(a)
        return c


gf = GF2_191()

a_str = "11111100010010010001110001001110110011111001000011100110011111111010101010100101101010101000101000010110111110011111010110100111111001100000110011101010011000110001000111100111110111110110010"
b_str = "11000101110100011100001001101110111010111110111101110110011110010110101000010110010111001000000010111001001010010101111011010101001111010000100000011011100101000000001011001001011010011011001"
n_str = "00010000101011001001000101111111010101001100100001101000000001101101010110110110111111110111011111100011010110111000110101101110011110111100111100111101110001000010111001010111100011110000110"

a = gf.bin_to_list(a_str)
b = gf.bin_to_list(b_str)
n = gf.bin_to_list(n_str)

start_time = time.time()
result_add = ''.join(map(str, gf.add(a, b)))
end_time = time.time()
print(" a + b:", result_add)
print("Час виконання додавання:", end_time - start_time, "секунд")

start_time = time.time()
result_mul = gf.multiply(a, b)
end_time = time.time()
result_mul_str = ''.join(map(str, result_mul))
print("a * b:", result_mul_str)
print("Час виконання множення:", end_time - start_time, "секунд")

start_time = time.time()
result_trace = str(gf.trace(a))
end_time = time.time()
print("Слід a:", result_trace)
print("Час виконання сліду:", end_time - start_time, "секунд")

start_time = time.time()
result_square = ''.join(map(str, gf.square(a)))
end_time = time.time()
print("a^2:", result_square)
print("Час виконання піднесення до квадрату:", end_time - start_time, "секунд")

start_time = time.time()
inverse = gf.inverse(a)
end_time = time.time()

inverse_str = gf.list_to_bin(inverse)
print("a^(-1):", inverse_str)
print("Час виконання обчислення оберненого елемента:", end_time - start_time, "секунд")

start_time = time.time()
result_power = gf.power(a, n)
end_time = time.time()

result_power_str = gf.list_to_bin(result_power)
print("a^n:", result_power_str)
print("Час виконання піднесення до степеня:", end_time - start_time, "секунд")



print(f" \n Очікуванні результати \n"
      f" a+b = 00111001100110001101111000100000001001000111111110010000000001101100000010110011111101100000101010101111110100001010101101110010110110110000010011110001111101110001001100101110101101101101011 \n"
      f" a*b = 01101110101011111100110100011111100010101010111010110100111001101111101001101111011100011011110000011100001111010100000011001010011101011000111000111101100100011011010011111111000000010101011 \n"
      f" a^2 =  \n"
      f" a^(-1)=  \n"
      f" a^n=  ")
