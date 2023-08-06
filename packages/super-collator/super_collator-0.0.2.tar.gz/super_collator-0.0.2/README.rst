==============
Super Collator
==============

.. |py39| image:: docs/_images/tox-py39.svg

.. |py310| image:: docs/_images/tox-py310.svg

.. |py311| image:: docs/_images/tox-py311.svg

.. |pypy38| image:: docs/_images/tox-pypy38.svg

.. |coverage| image:: docs/_images/coverage.svg

|py39| |py310| |py311| |pypy38| |coverage|

Collates textual sources with relaxed spelling.  Uses Gotoh's variant of the
Needleman-Wunsch sequence alignment algorithm.

.. code-block:: shell

   $ pip install super-collator

.. code-block:: python

   >>> from super_collator.strategy import CommonNgramsStrategy
   >>> from super_collator.token import SingleToken
   >>> from super_collator.super_collator import align, to_table

   >>> a = "Lorem ipsum dollar amat adipiscing elit"
   >>> b = "qui dolorem ipsum quia dolor sit amet consectetur adipisci velit"
   >>>
   >>> a = [SingleToken(s) for s in a.split()]
   >>> b = [SingleToken(s) for s in b.split()]
   >>>
   >>> c, score = align(a, b, CommonNgramsStrategy(2))
   >>> print(to_table(c))  # doctest: +NORMALIZE_WHITESPACE
   -   Lorem   ipsum -    dollar -   amat -           adipiscing elit
   qui dolorem ipsum quia dolor  sit amet consectetur adipisci   velit

Documentation: https://cceh.github.io/super-collator/

PyPi: https://pypi.org/project/super-collator/
