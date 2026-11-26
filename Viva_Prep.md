# Viva Preparation Guide — Eigenvalues & Eigenvectors (M3 Project)

- **Student:** SIDDHANT KUMAR THAKUR (`E25B070826`)
- **Course:** Linear Algebra and Calculus (M3)
- **Matrix Used:** $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$ ($\lambda_1 = 3, \mathbf{v}_1 = (1, 1)$; $\lambda_2 = 1, \mathbf{v}_2 = (1, -1)$)

---

## (a) Plain-Language Walkthrough of Every Scene's Code

### Shared Infrastructure (`E25B070826_Code/helpers/`)
- **`helpers/config.py`**: Stores all constants in one place so every scene shares identical colors (`EIG1_COLOR` orange `#FB923C` for $\mathbf{v}_1$, `EIG2_COLOR` teal `#2DD4BF` for $\mathbf{v}_2$, `ORD_VEC_COLOR` blue `#60A5FA` for ordinary inputs, `TRANS_VEC_COLOR` yellow `#FACC15` for transformed outputs), font sizes, matrix `MATRIX_A`, and student metadata.
- **`helpers/visuals.py`**: Reusable visual helpers:
  - `make_plane(...)`: Creates a Manim `NumberPlane` with subtle grid lines and labeled axes.
  - `make_axis_labels(plane)`: Places crisp `MathTex` $x$ and $y$ labels near the positive ends of the axes.
  - `make_card(mobject, ...)`: Wraps text/equations in a dark `RoundedRectangle` card so labels remain legible even over coordinate grid lines.
  - `make_plane_vector(plane, coords, color)`: Draws an `Arrow` from the origin `(0, 0)` to `coords` using `plane.c2p(...)` (coordinate-to-point conversion).
  - `make_eigen_lines(plane)`: Draws dashed invariant lines along $y = x$ (orange) and $y = -x$ (teal).
  - `make_scene_header(title_text, badge_text)`: Standardizes top-left title and top-right badge placement.
- **`helpers/voice.py`**: Defines `KokoroSpeechService(SpeechService)` (offline neural TTS via `kokoro-onnx`, voice `am_michael`, speed `0.96`), plus `EdgeTTSSpeechService` and `GTTSService` fallbacks, so `VoiceoverScene` automatically generates and caches `.mp3` clips and synchronizes `with self.voiceover(...)` blocks.
- **`main.py`**: Orchestrates rendering all 6 scenes at 1080p30 via `manim -qh --fps 30` and concatenates them with `ffmpeg` (`libx264`, `-crf 21`, `yuv420p`, AAC audio) into `E25B070826_Video.mp4`.

### Scene 1 — `scene1_hook.py` (`Scene1Hook`)
1. **Opening Frame**: Displays `COURSE_NAME`, `PROJECT_TITLE`, `PROJECT_SUBTITLE`, a mini two-vector motif (`m_arrow1`, `m_arrow2`, and `Av = λv`), and the student card (`SIDDHANT KUMAR THAKUR | ID: E25B070826`) using `Write`, `FadeIn`, and `GrowArrow`.
2. **Grid & Arrows**: Fades out the title card and draws an oversized `NumberPlane` (`grid`) plus static numbered `static_axes` and 10 blue arrows (`LaggedStart` of `GrowArrow`). An oversized grid (`[-10, 10] x [-8, 8]`) prevents dark empty gaps at screen edges when the grid stretches.
3. **Transformation Hook**: Uses `ApplyMatrix(MATRIX_A, grid)` simultaneously with `Transform(a, ta)` for every arrow (using `Transform` keeps arrowheads undistorted instead of squishing polygon tips). Ends with the yellow question banner: *"Is there any direction that survives without rotating?"*

### Scene 2 — `scene2_concept.py` (`Scene2Concept`)
1. **Left Geometric Contrast Panel**: Inside a framed `mini_plane`, draws an ordinary input vector $\mathbf{x}$ (blue) and its transformed output $A\mathbf{x}$ (yellow) with an `Arc` (`angle_arc`) showing rotation (`"Rotated!"`). Then transitions to an eigenvector $\mathbf{v}$ along the dashed orange line $y = x$, showing $A\mathbf{v} = \lambda\mathbf{v}$ staying collinear (`"Same direction!"`).
2. **Right Formal Definition & Symbol Key**: Builds $T(\mathbf{x}) = A\mathbf{x}$ and $A\mathbf{v} = \lambda\mathbf{v},\; \mathbf{v} \neq \mathbf{0}$ inside a `SurroundingRectangle`, followed by a `make_card` legend defining $A$, $I$, $\mathbf{v}$, and $\lambda$ before they are used algebraically.
3. **Learning Objective**: Fades in the blue bottom card containing the exact one-sentence learning objective.

### Scene 3 — `scene3_intuition.py` (`Scene3Intuition`)
1. **Warped Grid & Unit Circle**: Briefly applies `ApplyMatrix(MATRIX_A, warped_grid)` as visual context, then overlays `unit_circle` (`Circle(radius=1.0)`) on the static plane.
2. **ValueTracker Sweep**: `theta_tracker = ValueTracker(0.0)` drives `always_redraw` objects:
   - `v_arrow` ($\mathbf{v}(\theta) = (\cos\theta, \sin\theta)$ in blue)
   - `av_arrow` ($A\mathbf{v}(\theta)$ in yellow)
   - `angle_sector` (live `Arc` between $\mathbf{v}$ and $A\mathbf{v}$, turning green near alignment and disappearing when $|\Delta\theta| < 0.025$ rad)
   - `hud` (live telemetry card displaying input angle, $\angle(\mathbf{v}, A\mathbf{v})$, and length scale $\|A\mathbf{v}\|/\|\mathbf{v}\|$).
3. **Alignment Highlights**: Pauses and triggers `Flash` + `Dot` markers at $\theta = 45^\circ, 135^\circ, 225^\circ, 315^\circ$.
4. **Invariant Lines**: Draws `make_eigen_lines(plane)` and animates $(1,1) \mapsto 3(1,1) = (3,3)$ along $y = x$ and $(1,-1) \mapsto 1(1,-1)$ along $y = -x$.

### Scene 4 — `scene4_example.py` (`Scene4WorkedExample`)
1. **Act 4A — Rearrangement & Singularity Diagram**:
   - Left: Uses `TransformMatchingTex` to transform $A\mathbf{v} = \lambda\mathbf{v}$ into $A\mathbf{v} = \lambda I\mathbf{v}$ and then $(A - \lambda I)\mathbf{v} = \mathbf{0},\; \mathbf{v} \neq \mathbf{0}$, paired with a `det_reason_card` explaining why invertibility fails to produce nonzero solutions.
   - Right: A `sing_plane` animates a unit square (`sing_square`) squishing onto the 1D line $y = -x$ (`squished_line`) under the singular matrix $A - 3I = [[-1, 1], [1, -1]]$, while nonzero $\mathbf{v} = (1, 1)$ collapses to `zero_dot` at the origin (`Flash`).
2. **Act 4B — Characteristic Equation**: Writes one `MathTex` line at a time (`c1` through `c5`) from $A - \lambda I$ to $\lambda^2 - 4\lambda + 3 = 0$ and $(\lambda - 1)(\lambda - 3) = 0$, ending with color-coded badges $\lambda_1 = 3$ (orange) and $\lambda_2 = 1$ (teal).
3. **Act 4C — Null Spaces & Verification**: Two side-by-side cards solve $(A - 3I)\mathbf{v} = \mathbf{0}$ and $(A - 1I)\mathbf{v} = \mathbf{0}$, yielding $\mathbf{v}_1 = (1, 1)$ and $\mathbf{v}_2 = (1, -1)$, and verify both by direct matrix-vector multiplication in green.

### Scene 5 — `scene5_interpretation.py` (`Scene5Interpretation`)
1. **Eigen-Stretching**: Draws $y = x$ and $y = -x$ along with $\mathbf{v}_1 = (1, 1)$ and $\mathbf{v}_2 = (1, -1)$. Animates $\mathbf{v}_1 \mapsto 3\mathbf{v}_1 = (3, 3)$ and flashes $\mathbf{v}_2 = (1, -1)$ unchanged, reinforcing pure stretching with zero rotation.
2. **Unit Square → Parallelogram**: Creates a shaded cyan `Polygon` for the unit square $[(0,0), (1,0), (1,1), (0,1)]$ and basis arrows $\mathbf{e}_1, \mathbf{e}_2$. Applies `ApplyMatrix(MATRIX_A, grid)` while transforming the square into the parallelogram $[(0,0), (2,1), (3,3), (1,2)]$ and updating the area cards from `1` to $|\det(A)| = 3 = \lambda_1 \cdot \lambda_2$.

### Scene 6 — `scene6_summary.py` (`Scene6SummaryCredits`)
1. **3-Point Summary**: Sequentially reveals three color-coded takeaway cards (`card1`, `card2`, `card3`), each paired with a mini vector/equation/polygon diagram.
2. **Credits Frame**: Fades into `credits_card` listing student name and ID, references (3Blue1Brown Ch. 14, Strang Ch. 6, M3 notes), music status (none), AI disclosure, Kokoro ONNX TTS engine, and SymPy/NumPy verification.

---

## (b) Full Mathematical Derivations & Matrix Cases

### 1. Derivation for $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$
1. **Definition**: $A\mathbf{v} = \lambda\mathbf{v}$ with $\mathbf{v} \neq \mathbf{0}$.
2. **Insert Identity**: Write $\lambda\mathbf{v} = \lambda I\mathbf{v}$ because you cannot subtract a scalar $\lambda$ from a $2\times 2$ matrix $A$ directly. Thus:
   $$A\mathbf{v} - \lambda I\mathbf{v} = \mathbf{0} \implies (A - \lambda I)\mathbf{v} = \mathbf{0}.$$
3. **Why $\det(A - \lambda I) = 0$**:
   - Suppose $\det(A - \lambda I) \neq 0$. Then $(A - \lambda I)$ is invertible, so multiplying both sides on the left by $(A - \lambda I)^{-1}$ gives:
     $$\mathbf{v} = (A - \lambda I)^{-1}\mathbf{0} = \mathbf{0}.$$
   - That contradicts $\mathbf{v} \neq \mathbf{0}$! Equivalently, by the Invertible Matrix Theorem, a homogeneous linear system $M\mathbf{v} = \mathbf{0}$ has a non-trivial solution ($\mathbf{v} \neq \mathbf{0}$) **if and only if** $M$ is singular, i.e., $\det(M) = 0$ (geometrically, $M$ squishes area to zero so a nonzero direction collapses onto $\mathbf{0}$).
4. **Characteristic Equation**:
   $$A - \lambda I = \begin{bmatrix} 2 - \lambda & 1 \\ 1 & 2 - \lambda \end{bmatrix}$$
   $$\det(A - \lambda I) = (2 - \lambda)^2 - 1^2 = (\lambda^2 - 4\lambda + 4) - 1 = \lambda^2 - 4\lambda + 3 = 0.$$
   Factoring gives $(\lambda - 1)(\lambda - 3) = 0$, so $\lambda_1 = 3$ and $\lambda_2 = 1$.
   *(Quick sanity check: $\text{trace}(A) = 2 + 2 = 4 = 3 + 1 = \lambda_1 + \lambda_2$, and $\det(A) = 4 - 1 = 3 = 3 \cdot 1 = \lambda_1 \lambda_2$.)*
5. **Eigenspaces**:
   - For $\lambda_1 = 3$: $(A - 3I)\mathbf{v} = \begin{bmatrix} -1 & 1 \\ 1 & -1 \end{bmatrix}\begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \implies -x + y = 0 \implies y = x$. Basis eigenvector: $\mathbf{v}_1 = (1, 1)$ (any $c(1,1)$ with $c \neq 0$ works).
   - For $\lambda_2 = 1$: $(A - I)\mathbf{v} = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}\begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \implies x + y = 0 \implies y = -x$. Basis eigenvector: $\mathbf{v}_2 = (1, -1)$.
6. **Substitution Check**:
   - $A\begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 2(1)+1(1) \\ 1(1)+2(1) \end{bmatrix} = \begin{bmatrix} 3 \\ 3 \end{bmatrix} = 3\begin{bmatrix} 1 \\ 1 \end{bmatrix}$.
   - $A\begin{bmatrix} 1 \\ -1 \end{bmatrix} = \begin{bmatrix} 2(1)+1(-1) \\ 1(1)+2(-1) \end{bmatrix} = \begin{bmatrix} 1 \\ -1 \end{bmatrix} = 1\begin{bmatrix} 1 \\ -1 \end{bmatrix}$.

### 2. What Happens for Other $2\times 2$ Matrices?
- **Negative eigenvalues ($\lambda < 0$)**: The vector stays on its span line, stretches by $|\lambda|$, and **flips $180^\circ$ to the opposite direction** (e.g., reflection across an axis has $\lambda = -1$).
- **Zero eigenvalue ($\lambda = 0$)**: $A\mathbf{v} = 0\mathbf{v} = \mathbf{0}$, meaning $\mathbf{v}$ lies in the null space of $A$ and gets crushed to the origin; $\det(A) = 0$.
- **Complex eigenvalues ($\lambda = a \pm bi,\; b \neq 0$)**: For example, a $90^\circ$ rotation matrix $\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$ has $\lambda^2 + 1 = 0 \implies \lambda = \pm i$. Geometrically, **no real direction stays on its own line** in $\mathbb{R}^2$; complex eigenvectors live in $\mathbb{C}^2$ and correspond to rotation + scaling spirals.
- **Repeated eigenvalues (algebraic multiplicity 2)**:
  - *Full geometric multiplicity (2)*: e.g. $cI = \begin{bmatrix} 3 & 0 \\ 0 & 3 \end{bmatrix}$ — every nonzero vector is an eigenvector (pure uniform scaling).
  - *Defective matrix (geometric multiplicity 1)*: e.g. a shear $\begin{bmatrix} 2 & 1 \\ 0 & 2 \end{bmatrix}$ has $\lambda = 2$ twice, but only a 1D eigenspace $\text{span}\{(1, 0)\}$ — space shears so there aren't two linearly independent eigenvectors.

---

## (c) 15 Likely Viva Questions & Model Answers

1. **Q: Why must an eigenvector be nonzero ($\mathbf{v} \neq \mathbf{0}$)?**  
   **A:** Because $A\mathbf{0} = \mathbf{0} = \lambda\mathbf{0}$ holds trivially for *every* matrix $A$ and *every* scalar $\lambda$, so $\mathbf{0}$ defines no direction and would make every number an eigenvalue.
2. **Q: If $\mathbf{v}$ is an eigenvector for $\lambda$, is $5\mathbf{v}$ or $-\mathbf{v}$ also an eigenvector?**  
   **A:** Yes. $A(c\mathbf{v}) = c(A\mathbf{v}) = c(\lambda\mathbf{v}) = \lambda(c\mathbf{v})$ for any nonzero scalar $c$. All scalar multiples of $\mathbf{v}$ (plus $\mathbf{0}$) form the **eigenspace** $E_\lambda = \ker(A - \lambda I)$.
3. **Q: Why do we write $A\mathbf{v} = \lambda I\mathbf{v}$ before factoring out $\mathbf{v}$?**  
   **A:** $A$ is a $2\times 2$ matrix and $\lambda$ is a scalar, so $A - \lambda$ is undefined. Inserting $I$ turns $\lambda$ into the matrix $\lambda I$ without changing $\lambda\mathbf{v}$.
4. **Q: Explain geometrically why $\det(A - \lambda I) = 0$ is necessary.**  
   **A:** We want a nonzero vector $\mathbf{v}$ that $(A - \lambda I)$ maps to $\mathbf{0}$. A linear map sends a nonzero vector to $\mathbf{0}$ only if it collapses dimension (squishes area to zero), which means its determinant must be zero.
5. **Q: Why did our matrix $A = [[2,1],[1,2]]$ end up with orthogonal eigenvectors $(1,1)$ and $(1,-1)$?**  
   **A:** Because $A$ is **real symmetric** ($A^T = A$). By the Spectral Theorem, eigenvectors of distinct eigenvalues of a symmetric matrix are always orthogonal: $(1,1)\cdot(1,-1) = 1 - 1 = 0$.
6. **Q: What is the difference between a linear transformation rotating vectors and having complex eigenvalues?**  
   **A:** Our matrix $A$ rotated *most* vectors (like $(1,0) \to (2,1)$ by $26.57^\circ$), yet still had two real invariant lines. Pure rotations (like $90^\circ$) rotate *every* vector, so they have no real eigenvectors and yield complex conjugate eigenvalues $\pm i$.
7. **Q: How are the trace and determinant related to eigenvalues?**  
   **A:** $\text{trace}(A) = \sum \lambda_i$ and $\det(A) = \prod \lambda_i$. Here $\text{trace}(A) = 2+2 = 4 = 3+1$, and $\det(A) = 4-1 = 3 = 3\times 1$.
8. **Q: In Scene 5, why does the parallelogram area equal $\lambda_1 \lambda_2 = 3$?**  
   **A:** A linear map scales all areas by $|\det(A)|$. Since $\det(A) = \lambda_1\lambda_2 = 3\cdot 1 = 3$, the unit square of area $1$ maps to a parallelogram of area $3$. (In the eigenbasis, the transformation is diagonal $\text{diag}(3,1)$, stretching one eigen-axis by 3 and the other by 1.)
9. **Q: What happens if an eigenvalue is $\lambda = 1$, like $\lambda_2 = 1$ here?**  
   **A:** Vectors along $\mathbf{v}_2 = (1,-1)$ are completely fixed points of the transformation: $A\mathbf{v}_2 = \mathbf{v}_2$ (no rotation, no length change).
10. **Q: What happens if an eigenvalue is $\lambda = -2$?**  
    **A:** Vectors in that eigenspace stay on the same line, double in length, and point in the opposite direction.
11. **Q: Can two different eigenvalues share the same nonzero eigenvector?**  
    **A:** No. If $A\mathbf{v} = \lambda_1\mathbf{v}$ and $A\mathbf{v} = \lambda_2\mathbf{v}$, then $(\lambda_1 - \lambda_2)\mathbf{v} = \mathbf{0}$. Since $\mathbf{v} \neq \mathbf{0}$, we must have $\lambda_1 = \lambda_2$.
12. **Q: What is the difference between algebraic multiplicity and geometric multiplicity?**  
    **A:** Algebraic multiplicity is how many times $\lambda$ is a root of $\det(A - \lambda I) = 0$. Geometric multiplicity is $\dim(\ker(A - \lambda I))$. Always $1 \le \text{geom. mult.} \le \text{alg. mult.}$. Here both equal $1$ for $\lambda=3$ and $\lambda=1$.
13. **Q: What is diagonalization and how does our example diagonalize?**  
    **A:** Since $(1,1)$ and $(1,-1)$ are linearly independent, $A = PDP^{-1}$ where $P = \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$ and $D = \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix}$. This turns computing $A^k$ into simply $P D^k P^{-1}$.
14. **Q: Name one real-world engineering application of eigenvalues and eigenvectors.**  
    **A:** Principal Component Analysis (PCA) in data science (eigenvectors of the covariance matrix give principal axes of variance), vibration/natural frequencies in mechanical structures, and Google's PageRank (principal eigenvector of the link matrix).
15. **Q: How did you verify that every number in your animation is mathematically exact?**  
    **A:** By running `verify_math.py` using SymPy (exact symbolic determinant, polynomial factoring, null spaces, substitution) and NumPy (eigenvalues/eigenvectors and angle-sweep check confirming $0^\circ$ error at $45^\circ, 135^\circ, 225^\circ, 315^\circ$).

---

## (d) Code Design Choices an Examiner Could Ask About

1. **Why render each scene separately and concatenate with `ffmpeg` instead of one giant `construct()`?**
   - Modularity: each of the 6 scenes is an independent `VoiceoverScene` class (`scene1_hook.py`–`scene6_summary.py`), so fixing one scene's layout only re-renders that scene rather than all 5+ minutes.
   - Final `ffmpeg` concat with `-c:v libx264 -crf 21 -pix_fmt yuv420p -c:a aac -movflags +faststart` guarantees uniform timestamps, smooth audio continuity, and a compact <100 MB MP4.
2. **Why `Transform(arrow, target_arrow)` instead of `ApplyMatrix(MATRIX_A, arrow)`?**
   - `ApplyMatrix` warps the polygon vertices of an `Arrow` tip, distorting the arrowhead when scaling is anisotropic ($3\times$ vs $1\times$). Using `ApplyMatrix` on the background `NumberPlane` while `Transform`-ing each `Arrow` to `make_plane_vector(plane, MATRIX_A @ c)` preserves razor-sharp arrowheads while keeping exact endpoint math.
3. **Why an oversized background `NumberPlane` (`[-10, 10] x [-8, 8]`) paired with static labeled axes?**
   - If you apply `MATRIX_A` to a screen-sized `[-6, 6] x [-4, 4]` grid, its transformed corners pull inward and leave blank ungridded triangles at the edges. An oversized background grid fills the entire 16:9 frame even after transformation, while keeping tick numbers on the static reference axes prevents numbers from flying off-screen or overlapping.
4. **Why `ValueTracker` + `always_redraw` in Scene 3?**
   - Rather than hardcoding discrete snapshots, a single continuous scalar `theta_tracker` drives $\mathbf{v}(\theta)$, $A\mathbf{v}(\theta)$, the angle sector `Arc`, and the telemetry HUD simultaneously every frame, visually proving that $\angle(\mathbf{v}, A\mathbf{v}) = 0^\circ$ occurs *only* at the four eigen-angles around the unit circle.
5. **Why `KokoroSpeechService` (offline ONNX) via `manim-voiceover`?**
   - `manim-voiceover` automatically measures each spoken cue's duration (`tracker.duration`) so animations never overrun or lag behind narration, while Kokoro ONNX produces calm, natural neural speech completely offline with deterministic caching.
6. **Why no background music?**
   - Skipping background music guarantees 100% vocal clarity and avoids any third-party music licensing ambiguity for academic submission.
