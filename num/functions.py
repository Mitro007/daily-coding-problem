# Given a real number n, find the square root of n. For example, given n = 9, return 3.
def square_root(n: int, tolerance: float) -> float:
    assert n >= 0, "n must be positive"
    prev_guess: float = 0.0
    new_guess: float = n / 2

    while abs(new_guess - prev_guess) > tolerance:
        prev_guess = new_guess
        new_guess = 0.5 * (prev_guess + n / prev_guess)

    return new_guess
