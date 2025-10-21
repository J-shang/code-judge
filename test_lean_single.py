import requests

code1 = r'''
import Mathlib
import Aesop
set_option maxHeartbeats 0
open BigOperators Real Nat Topology Rat

/-- The volume of a cone is given by the formula $V = \frac{1}{3}Bh$, where $B$ is the area of the base and $h$ is the height. The area of the base of a cone is 30 square units, and its height is 6.5 units. What is the number of cubic units in its volume? Show that it is 65.-/
theorem mathd_algebra_478 (b h v : ℝ) (h₀ : 0 < b ∧ 0 < h ∧ 0 < v) (h₁ : v = 1 / 3 * (b * h))
    (h₂ : b = 30) (h₃ : h = 13 / 2) : v = 65 := by
  -- Use the given equality: v = (1/3) * (b * h)
  rw h₁
  -- Now we have: v = (1/3) * (b * h)
  -- Substitute b = 30 and h = 13/2
  rw h₂
  rw h₃
  -- Now we have: v = (1/3) * (30 * (13 / 2))
  -- Compute: 30 * (13 / 2) = (30 * 13) / 2 = 390 / 2 = 195
  simp [mul_div_assoc, mul_comm, mul_left_comm]
  -- Now: v = (1/3) * 195 = 195 / 3 = 65
  simp [div_eq_mul_inv, mul_assoc]
  -- Now: v = 65
  rfl
'''

code2 = r'''
import Mathlib
import Aesop
set_option maxHeartbeats 0
open BigOperators Real Nat Topology Rat

/-- The volume of a cone is given by the formula $V = \frac{1}{3}Bh$, where $B$ is the area of the base and $h$ is the height. The area of the base of a cone is 30 square units, and its height is 6.5 units. What is the number of cubic units in its volume? Show that it is 65.-/
theorem mathd_algebra_478 (b h v : ℝ) (h₀ : 0 < b ∧ 0 < h ∧ 0 < v) (h₁ : v = 1 / 3 * (b * h))
    (h₂ : b = 30) (h₃ : h = 13 / 2) : v = 65 := by
  -- Substitute the values of b and h into the formula
  rw h₁
  rw h₂
  rw h₃
  -- Now we have: v = (1/3) * (30 * (13 / 2))
  -- Use norm_num to evaluate the expression numerically
  norm_num
'''

code3 = r'''
import Mathlib

/- Given that the product \( a \cdot b \cdot c = 1 \), what is the value of the following expression?
$$
\frac{a}{a b + a + 1} + \frac{b}{b c + b + 1} + \frac{c}{c a + c + 1}
$$-/
theorem algebra_4013 {a b c : ℝ} (h : a * b * c = 1) (haux : 1 + a + a * b ≠ 0) :
a / (a * b + a + 1) + b / (b * c + b + 1) + c / (c * a + c + 1) = 1 := by
-- need ne_zero condition to perform division
have : a * b * c ≠ 0 := by rw [h]; norm_num
have ha : a ≠ 0 := left_ne_zero_of_mul <| left_ne_zero_of_mul this
have hb : b ≠ 0 := right_ne_zero_of_mul <| left_ne_zero_of_mul this
-- Multiply the second fraction by \(a\).
conv => lhs; lhs; rhs; rw [← mul_div_mul_left _ _ ha]
-- Multiply the third fraction by \(ab\).
conv => lhs; rhs; rw [← mul_div_mul_left _ _ (mul_ne_zero ha hb)]
-- Thus, we get:
-- \[
-- \frac{a}{ab + a + 1} + \frac{ab}{abc + ab + a} + \frac{abc}{abca + abc + ab}
-- \]
rw [show a * (b * c + b + 1) = a*b*c + a*b + a by ring]
rw [show a*b*(c * a + c + 1) = a*b*c*a + a*b*c + a*b by ring]
-- **Simplify the expression using \(abc = 1\):**
rw [h, one_mul]
ring_nf
-- **Combine the terms with the same denominator:**
rw [← add_mul]
nth_rw 2 [← one_mul (1 + a + a * b)⁻¹]
rw [← add_mul, show a * b + a + 1 = 1 + a + a * b by ring]
exact mul_inv_cancel₀ haux
'''


submissions = [
    {
        "type": "lean",
        "solution": code1,
    },
    {
        "type": "lean",
        "solution": code3,
    },
]

data = {
        'type': 'batch',
        "submissions": submissions
    }

response = requests.post("http://0.0.0.0:8088/run/long-batch", json=data)
result = response.json()
import json
print(json.dumps(result, indent=2))
