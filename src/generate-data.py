import random

def generate_dry_inflow(n=96):
    values = []
    x = 1.0  # start near the "normal" value

    for _ in range(n):
        # random small step, so we don't jump from 0.5 to 3.0 in one go
        step = random.uniform(-0.4, 0.4)
        x += step

        # gently pull the value back toward 1 so it's the most common
        x += (1.0 - x) * 0.1

        # clip to [0.5, 3.0]
        x = max(0.5, min(3.0, x))

        # round for nicer numbers
        values.append(round(x, 2))

    return values

dry_inflow = generate_dry_inflow()
print(dry_inflow)

# import random

# def generate_inflow(n=96):
#     values = []
#     x = 0.3  # start at the typical value

#     for _ in range(n):
#         # allow faster movement, but still not 0.3 -> 20.0 in 1 step
#         step = random.uniform(-4.0, 4.0)
#         x += step

#         # pull back toward 0.3 so it's the most common value
#         x += (0.3 - x) * 0.3

#         # clip to [0.1, 20.0]
#         x = max(0.1, min(20.0, x))

#         values.append(round(x, 2))

#     return values

# dry_inflow = generate_inflow()
# print(dry_inflow)
