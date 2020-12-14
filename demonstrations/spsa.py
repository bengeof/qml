r""".. _spsa:

Optimization using SPSA
=======================

PennyLane allows computing quantum gradients using  parameter-shift rules.

For quantum circuits that have multiple free parameters, using the
parameter-shift rule to compute quantum gradients involves computing the
partial derivatives of the quantum function w.r.t. each free parameter. These
partial derivatives are then used to apply the product rule when computing the
quantum gradient (`see parameter-shift rules
<https://pennylane.ai/qml/glossary/parameter_shift.html>`_). For qubit
operations that are generated by one of the Pauli matrices, each partial
derivative computation will involve two quantum circuit evaluations with a
positive and a negative shift in the parameter values.

As in such cases there would be two circuit evaluation for each free parameter,
the number of overall quantum circuit executions for computing a quantum
gradient scales linearly with the number of free parameters: :math:`O(k)` with
:math:`k` being the number of free parameters. This scaling can be very costly
for optimization tasks where many free pramaeters are considered in the quantum
circuit. For the overall optimization this scaling gives :math:`O(k*n)` quantum
circuit evaluations with :math:`n` being the number of optimization steps taken.

There are, however, certain optimization techniques that are gradient-free and
hence offer othen approach analytically computing the gradients of quantum
circuits.

One of such techniques is called Simultaneous perturbation stochastic
approximation (SPSA), an optimization method that involves approximating the
gradient of the cost function at each iteration step. This technique involves
only two quantum circuit executions per iteration step, regardless of the
number of free parameters. Therefore the overall number of circuit executions
would be :math:`O(n')` where :math:`n'` is the number of optimization steps taken when
using SPSA. This technique was also found to be robust against noise, making it
a great optimization method in the NISQ era.

Let's have a look at the details of how exactly this technique works.

Simultaneous perturbation stochastic approximation (SPSA)
---------------------------------------------------------

SPSA is a general method for minimizing differentiable multivariate functions
mostly tailored towards those functions for which evaluating the gradient is
not available.

SPSA provides a stochastic method for approximating the gradient of a
multivariate differentiable cost function without having to evaluate the
gradient of the function. To approximate the gradient, the cost function is
evaluated twice using perturbed parameter vectors: every component of the
original parameter vector is simultaneously shifted with a randomly generated
value. This is in contrast to finite-differences methods where for each
evaluation only one component of the parameter vector is shifted.

Similar to gradient-based approaches such as gradient descent, SPSA offers an
iterative optimization algorithm. We consider a differentiable cost function
:math:`L(\theta)` where :math:`\theta` is a :math:`p-dimensional` vector and where the
optimization problem can be translated into  finding a :math:`\theta*` such that
:math:`\frac{\partial L}{\partial u} = 0`.  It is assumed that measurements of
:math:`L(\theta)` are available at various values of :math:`\theta`.

This is exactly the problem that we'd consider when optimizing quantum
functions!

.. figure:: ../demonstrations/spsa/spsa_opt.png
    :align: center
    :width: 60%

    ..

    A schematic of the search paths used by gradient descent with
    parameter-shift and SPSA in a low-noise setting.
    Image source: [#spall_overview]_.

Just like with gradient-based methods, we'd start with a :math:`\hat{\theta}_{0}`
initial parameter vector. After :math:`k` iterations, the :math:`k+1.` parameter iterates
can be obtained as

.. math:: \hat{\theta}_{k+1} = \hat{\theta}_{k} - a_{k}\hat{g}_{k}(\hat{\theta}_{k})

where :math:`\hat{g}_{k}` is the estimate of the gradient :math:`g(u) = \frac{
\partial L}{\partial \theta}` at the iterate :math:`\hat{\theta}_{k}` based on
prior measurements of the cost function and :math:`a_{k}` is a numeric
coefficient.

As previously mentioned, SPSA further takes into account the noisiness of the
result obtained when measuring function :math:`L`. Therefore, let's consider the
function :math:`y(\theta)=L(\theta) + noise`.

Using :math:`y`, the estimated gradient at each iteration step is expressed as

.. math:: \hat{g}_{ki} (\hat{\theta}_{k}) = \frac{y(\hat{\theta}_{k} +c_{k}\Delta_{k})
    - y(\hat{\theta}_{k} -c_{k}\Delta_{k})}{2c_{k}\Delta_{ki}}

where :math:`c_{k}` is a positive number and :math:`\Delta_{k} = (\Delta_{k_1},
\Delta_{k_2}, ..., \Delta_{k_p})^{T}` is the perturbation vector.  The
stochasticity of the technique comes from the fact that for each iteration step
:math:`k` the components of the :math:`\Delta_{k}` perturbation vector are randomly
generated using a zero-mean distribution. In most cases, the Bernoulli
distribution is used.

"""


##############################################################################
# References
# ----------
#
# .. [#spall_overview]
#
#    1. James C. Spall, "An Overview of the Simultaneous Perturbation Method for Efficient Optimization."
#    `<https://www.jhuapl.edu/SPSA/PDF-SPSA/Spall_An_Overview.PDF>`__, 1998