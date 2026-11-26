# Narration Script — Eigenvalues and Eigenvectors

- **Course:** Linear Algebra and Calculus (M3) — Internal Assessment Project (Option 1: Animation Video)
- **Student:** SIDDHANT KUMAR THAKUR (`E25B070826`)
- **Topic:** Eigenvalues and Eigenvectors (`A = [[2, 1], [1, 2]]`)
- **Target Pace:** ~145 words per minute (calm, clear voice)
- **Target Duration:** ~5:00 (estimated ~725 words across ~5:00 with visual pauses)

---

## Scene 1: Hook / Context (~30 s | ~72 words)

**Cue 1A — Opening Title Card (~6 s, ~14 words):**
> Welcome to this M3 Linear Algebra visual guide on eigenvalues and eigenvectors.

**Cue 1B — Grid & Arrow Transformation (~24 s, ~58 words):**
> Imagine the two-dimensional plane filled with vectors pointing in many directions. Now let us apply the matrix A, with entries two, one, one, two, to the entire plane. Watch closely as the grid warps. Almost every arrow tilts onto a completely new angle. That raises a natural question: is there any direction that survives the transformation without rotating?

---

## Scene 2: Concept Introduction (~40 s | ~95 words)

**Cue 2A — Linear Transformation & Formal Definition (~25 s, ~60 words):**
> A matrix A defines a linear transformation T of x equals A times x, moving each vector to a new position while keeping grid lines parallel and evenly spaced. An eigenvector is a nonzero vector v whose direction never changes under A. Instead, A times v equals lambda times v, where the scalar lambda is the eigenvalue that measures how much v stretches or shrinks.

**Cue 2B — Notation & Learning Objective (~15 s, ~35 words):**
> Here, A is our two-by-two matrix, I is the identity matrix, v is a nonzero vector, and lambda is a real number. By the end of this video, you will be able to explain eigenvectors and eigenvalues geometrically, and compute them for a two-by-two matrix.

---

## Scene 3: Visual Intuition (~60 s | ~145 words)

**Cue 3A — Rotating Test Vector & Angle Tracker (~35 s, ~85 words):**
> Before touching any algebra, let us test every direction around the unit circle. Here, the rotating arrow is our input vector v, and the yellow arrow is its output A times v. Notice the angle readout between them. Almost everywhere, A knocks the output off the input's line. Watch what happens at forty-five degrees: the angle drops to zero, and both arrows align! Continue rotating: they separate again, until one hundred thirty-five degrees, where the angle hits zero a second time.

**Cue 3B — The Two Invariant Lines (~25 s, ~60 words):**
> Sweeping the full circle reveals two special invariant lines. Along the orange line y equals x, every vector stays on its own line and stretches to three times its length. Along the teal line y equals minus x, vectors stay on their line completely unchanged, scaled by one. Everything else gets pulled away from its line.

---

## Scene 4: Worked Example (~100 s | ~232 words)

**Cue 4A — Setting up (A - lambda I)v = 0 (~35 s, ~80 words):**
> Now let us find those exact numbers algebraically for A equals two, one, one, two. Start from the definition: A v equals lambda v. Insert the identity matrix I so we can factor out v, giving A minus lambda I, all times v, equals zero. Why must the determinant of A minus lambda I equal zero? Because we need a nonzero vector v. If this matrix were invertible, the only solution would be v equals zero. Setting the determinant to zero makes the matrix singular, squishing space so a nonzero direction collapses to zero.

**Cue 4B — Characteristic Equation & Eigenvalues (~30 s, ~72 words):**
> Subtracting lambda along the diagonal gives two minus lambda, one, one, two minus lambda. Its determinant is two minus lambda squared, minus one. Expanding gives lambda squared minus four lambda plus three equals zero. Factoring into lambda minus one times lambda minus three equals zero yields two eigenvalues: lambda one equals three, and lambda two equals one.

**Cue 4C — Null Spaces & Verification (~35 s, ~80 words):**
> Let us solve for each eigenvector. For lambda one equals three, A minus three I has rows minus one, one and one, minus one. Both give minus x plus y equals zero, so y equals x, giving v one equals one, one. For lambda two equals one, A minus I has rows one, one and one, one, giving x plus y equals zero, so v two equals one, minus one. Substituting back confirms A times one, one equals three, three, and A times one, minus one equals one, minus one.

---

## Scene 5: Interpretation (~50 s | ~116 words)

**Cue 5A — Connecting Algebra to Geometry (~25 s, ~58 words):**
> Putting the algebra back on our grid, the vector one, one lies right along the orange line y equals x, stretching by three. The vector one, minus one lies along the teal line y equals minus x, scaled by one. Along these eigen-directions, the transformation acts purely as stretching, with zero rotation.

**Cue 5B — Unit Square & Determinant Area Scaling (~25 s, ~58 words):**
> Now watch the unit square, which starts with area one. Under A, its basis edges one, zero and zero, one map to two, one and one, two, forming a parallelogram. Its area is the determinant of A, which equals three. Notice that three equals three times one, the product of our two eigenvalues!

---

## Scene 6: Summary & Credits (~30 s | ~66 words)

**Cue 6A — Three Takeaways (~18 s, ~40 words):**
> To summarize: first, eigenvectors keep their direction while eigenvalues measure their scaling. Second, solve determinant of A minus lambda I equals zero for eigenvalues, then solve the null space for eigenvectors. Third, the determinant equals the product of the eigenvalues and gives the area scale factor.

**Cue 6B — Credits (~12 s, ~26 words):**
> Thank you for watching. Inspired by three-blue-one-brown and M3 Linear Algebra notes. Presented by Siddhant Kumar Thakur, Student ID E-two-five-B-zero-seven-zero-eight-two-six.

---

## Timing & Word Count Summary

| Scene | Title | Word Count | Est. Speech (~145 wpm) | Visual Pauses | Target Total |
|---|---|---:|---:|---:|---:|
| 1 | Hook / Context | 72 | ~30 s | ~2 s | ~32 s |
| 2 | Concept Introduction | 95 | ~39 s | ~2 s | ~41 s |
| 3 | Visual Intuition | 145 | ~60 s | ~2 s | ~62 s |
| 4 | Worked Example | 232 | ~96 s | ~4 s | ~100 s |
| 5 | Interpretation | 116 | ~48 s | ~2 s | ~50 s |
| 6 | Summary & Credits | 66 | ~27 s | ~3 s | ~30 s |
| **Total** | **All 6 Scenes** | **726** | **~300 s (5:00)** | **~15 s** | **~5:15** |
